# rating_pipeline_llama_v2.py
import os
import re
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# ENV / DISABLE COMPILERS
# --------------------------
BASE_TMP = "/tmp/giri/model-test"
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["TORCHINDUCTOR_DISABLE"] = "1"

os.environ["TORCHINDUCTOR_CACHE_DIR"] = f"{BASE_TMP}/torchinductor"
os.environ["TRITON_CACHE_DIR"] = f"{BASE_TMP}/triton"
os.environ["XDG_CACHE_HOME"] = f"{BASE_TMP}/xdg"
os.environ["HF_HOME"] = f"{BASE_TMP}/huggingface"
os.environ["TRANSFORMERS_CACHE"] = f"{BASE_TMP}/transformers"

for d in [
    os.environ["TORCHINDUCTOR_CACHE_DIR"],
    os.environ["TRITON_CACHE_DIR"],
    os.environ["XDG_CACHE_HOME"],
    os.environ["HF_HOME"],
    os.environ["TRANSFORMERS_CACHE"],
]:
    os.makedirs(d, exist_ok=True)

import torch._dynamo as dynamo
dynamo.config.suppress_errors = True
torch._dynamo.disable()

# --------------------------
# CONFIG
# --------------------------
MODEL_PATH = "/mnt/nas1/huggingface/llama-3.2-3b-instruct"
DATASET_PATH = "your_dataset.csv"
OUT_PATH = f"{BASE_TMP}/evaluated_llama.csv"
BATCH_SIZE = 2
MAX_NEW_TOKENS = 256

# Column names (single place to edit)
COL_TRANSCRIPT = "transcript"
COL_SUMMARY = "lama_summary"

# --------------------------
# Load model & tokenizer
# --------------------------
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)
device = model.device
print("Model loaded on", device)

# --------------------------
# Read dataset
# --------------------------
if os.path.isdir(DATASET_PATH):
    found = [f for f in os.listdir(DATASET_PATH) if f.lower().endswith(".csv")]
    if not found:
        raise SystemExit(f"No .csv found in {DATASET_PATH}")
    DATASET_PATH = os.path.join(DATASET_PATH, found[0])
    print("Auto-selected dataset:", DATASET_PATH)

df = pd.read_csv(DATASET_PATH)
if not {COL_TRANSCRIPT, COL_SUMMARY}.issubset(df.columns):
    raise SystemExit(f"CSV must have columns: {COL_TRANSCRIPT}, {COL_SUMMARY}")

# --------------------------
# Prompt template
# --------------------------
prompt_template = """Evaluate the following summary against the transcript.
Provide a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate).
Do NOT repeat the transcript or summary.
Output must be ONLY in this format:

Rating: <digit 1-5>
Explanation: <your explanation>

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Parser
# --------------------------
def parse_rating_and_explanation(text: str):
    if not text:
        return None, None
    s = text.strip()
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        return int(m.group(1)), s[m.end():].strip()
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        return int(m.group(1)), s[m.end():].strip()
    m = re.search(r"Explanation\s*[:\-]?\s*(.*)", s, re.DOTALL | re.IGNORECASE)
    if m:
        return None, m.group(1).strip()
    return None, s

def clean_explanation(text: str, max_len=800):
    if not text:
        return ""
    text = re.sub(r"Transcript:.*?Summary:", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"\b1\s*=\s*[^,.\n]*[,.\n]?\s*5\s*=\s*[^,.\n]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len] + (" ..." if len(text) > max_len else "")

# --------------------------
# Generate helper
# --------------------------
def generate_response(prompt, max_new_tokens=MAX_NEW_TOKENS):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.inference_mode():
        out = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_new_tokens,
            do_sample=False
        )
    return tokenizer.decode(out[0], skip_special_tokens=True).strip()

# --------------------------
# Run model batch
# --------------------------
all_raw = []
n = len(df)
for start in range(0, n, BATCH_SIZE):
    batch_df = df.iloc[start:start + BATCH_SIZE]
    prompts = [
        prompt_template.format(source=row[COL_TRANSCRIPT], summary=row[COL_SUMMARY])
        for _, row in batch_df.iterrows()
    ]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(device)
    pad_id = tokenizer.pad_token_id or tokenizer.eos_token_id
    input_lengths = (inputs["input_ids"] != pad_id).sum(dim=1).tolist()

    with torch.inference_mode():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False
        )

    for j, out in enumerate(outputs):
        in_len = input_lengths[j]
        gen_tokens = out[in_len:] if out.shape[0] > in_len else out
        decoded = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()
        all_raw.append(decoded if decoded else "[EMPTY]")

df["raw_evaluation"] = all_raw

# --------------------------
# Extract results with retry
# --------------------------
ratings, explanations = [], []
for i, raw in enumerate(df["raw_evaluation"]):
    row = df.iloc[i]
    rating, explanation = parse_rating_and_explanation(raw)

    attempts = 1
    while rating is None and attempts < 3:
        if attempts == 1:
            # rescue: extract rating only
            rescue_prompt = f"Extract only the rating (a single digit 1–5) from this text:\n\n{raw}"
            rescue_out = generate_response(rescue_prompt, max_new_tokens=16)
            m = re.search(r"\b([1-5])\b", rescue_out)
            if m:
                rating = int(m.group(1))
        else:
            # regenerate full response
            rescue_prompt = prompt_template.format(
                source=row[COL_TRANSCRIPT], summary=row[COL_SUMMARY]
            )
            rescue_out = generate_response(rescue_prompt)
            rating, explanation = parse_rating_and_explanation(rescue_out)
        attempts += 1

    explanations.append(clean_explanation(explanation))
    ratings.append(rating)

df["rating"] = ratings
df["explanation"] = explanations

# --------------------------
# Debug print
# --------------------------
for i in range(min(3, len(df))):
    print("---- ROW", i, "----")
    print("RAW:", repr(df.loc[i, "raw_evaluation"])[:400])
    print("RATING:", df.loc[i, "rating"])
    print("EXPLANATION:", df.loc[i, "explanation"][:300])
    print()

# --------------------------
# Save
# --------------------------
os.makedirs(BASE_TMP, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print("Saved:", OUT_PATH)