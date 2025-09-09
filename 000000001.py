# rating_pipeline_phi_v1.py
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
MODEL_PATH = "/mnt/nas1/huggingface/phi-3-mini-128k-instruct"   # change to your Phi model
DATASET_PATH = "your_dataset.csv"
OUT_PATH = f"{BASE_TMP}/evaluated_dataset_phi.csv"
BATCH_SIZE = 2
MAX_NEW_TOKENS = 256

# --------------------------
# Load model & tokenizer
# --------------------------
print("Loading Phi model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)
device = model.device
print("Model loaded on", device)

# --------------------------
# Dataset
# --------------------------
if os.path.isdir(DATASET_PATH):
    found = [f for f in os.listdir(DATASET_PATH) if f.lower().endswith(".csv")]
    if not found:
        raise SystemExit(f"No .csv found in {DATASET_PATH}")
    DATASET_PATH = os.path.join(DATASET_PATH, found[0])
    print("Auto-selected dataset:", DATASET_PATH)

df = pd.read_csv(DATASET_PATH)
if not {"transcript", "lama_summary"}.issubset(df.columns):
    raise SystemExit("CSV must contain columns: 'transcript' and 'lama_summary'")

# --------------------------
# Phi prompt template
# --------------------------
prompt_template = """<|system|>
You are an evaluator.
<|user|>
Evaluate the following summary against the transcript.
Provide a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate).
Do NOT repeat the transcript or summary.
Output must be STRICTLY in this format:

Rating: <digit>
Explanation: <your explanation>

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Robust parser
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    s = generated_text.strip()

    # strict "Rating: d" capture
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        explanation = re.sub(r"^Explanation\s*[:\-]?\s*", "", explanation, flags=re.IGNORECASE)
        return rating, explanation

    # bare digit at start
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    return None, s

def clean_explanation(text: str, max_len: int = 800):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[:max_len] + " ..."
    return text

# --------------------------
# Retry generator
# --------------------------
def generate_with_retry(prompt, max_retries=3):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    for attempt in range(max_retries):
        with torch.inference_mode():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False
            )
        gen_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        decoded = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

        rating, explanation = parse_rating_and_explanation(decoded)
        if rating is not None:
            return decoded, rating, explanation

        print(f"[WARN] Retry {attempt+1} failed. Raw: {decoded[:120]}")

    # If still failed after retries
    return decoded, None, None

# --------------------------
# Main loop
# --------------------------
raws, ratings, explanations = [], [], []

for idx, row in df.iterrows():
    prompt = prompt_template.format(source=row["transcript"], summary=row["lama_summary"])
    raw, rating, explanation = generate_with_retry(prompt)

    raws.append(raw)
    ratings.append(rating)
    explanations.append(clean_explanation(explanation))

df["raw_evaluation"] = raws
df["rating"] = ratings
df["explanation"] = explanations

# debug sample
for i in range(min(3, len(df))):
    print("---- ROW", i, "----")
    print("RAW OUTPUT:", repr(df.loc[i, "raw_evaluation"])[:400])
    print("RATING:", df.loc[i, "rating"])
    print("EXPLANATION:", df.loc[i, "explanation"][:300])
    print()

df.to_csv(OUT_PATH, index=False)
print("Saved evaluated CSV to:", OUT_PATH)