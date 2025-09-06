# rating_pipeline_clean.py
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

# explicitly disable torch dynamo
import torch._dynamo as dynamo
dynamo.config.suppress_errors = True
torch._dynamo.disable()

# --------------------------
# CONFIG - edit these
# --------------------------
MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"         # your local model folder
DATASET_PATH = "your_dataset.csv"                          # change to your csv path
OUT_PATH = f"{BASE_TMP}/evaluated_dataset.csv"
BATCH_SIZE = 2                                             # increase if memory allows
MAX_NEW_TOKENS = 256

# --------------------------
# Load model & tokenizer
# --------------------------
print("Loading model and tokenizer...")
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
# Read dataset (auto-find if a directory was given)
# --------------------------
if os.path.isdir(DATASET_PATH):
    # try to find a CSV inside the folder
    found = [f for f in os.listdir(DATASET_PATH) if f.lower().endswith(".csv")]
    if not found:
        raise SystemExit(f"No .csv found in directory {DATASET_PATH}. Please supply a file path.")
    DATASET_PATH = os.path.join(DATASET_PATH, found[0])
    print("Auto-selected dataset:", DATASET_PATH)

df = pd.read_csv(DATASET_PATH)
# expected columns: 'transcript' and 'lama_summary' (or rename below)
if not {"transcript", "lama_summary"}.issubset(df.columns):
    raise SystemExit("CSV must contain columns: 'transcript' and 'lama_summary'")

# --------------------------
# Prompt template (defined once)
# --------------------------
prompt_template = """Evaluate the following summary against the transcript.
Provide a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate).
Do NOT repeat the transcript or summary. Output must be in one of the forms (strict):
1) A single digit on the first line (e.g. `4`) followed by the explanation on the next lines
2) Or: `Rating: 4\\nExplanation: ...`

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Helper: robust parser
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    """
    Parse generated_text to extract rating (int 1-5) and explanation (string).
    Uses multiple patterns and avoids picking up digits from the prompt/help text.
    """
    s = generated_text.strip()

    # 1) Try exact start-of-output digit on its own line: "4\n..."
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # 2) Try "Rating: 4" (case-insensitive), capture and take remainder as explanation
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # 3) Try "4/5" style near start
    m = re.search(r"([1-5])\s*/\s*5", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # 4) Fallback: look for the first occurrence of digit 1-5 within the first ~200 chars,
    # but ignore occurrences that are followed by '=' (these are scale definitions).
    prefix = s[:200]
    for mm in re.finditer(r"([1-5])", prefix):
        idx_end = mm.end()
        # if an equals sign comes immediately after (scale like "1 = very..."), skip it
        after = s[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):
            continue
        rating = int(mm.group(1))
        explanation = s[idx_end:].strip()
        return rating, explanation

    # 5) No rating found
    return None, s.strip()

# small cleaner for explanation text
def clean_explanation(text: str, max_len: int = 800):
    if not text:
        return ""
    # remove any repeated prompt fragments that survived
    text = re.sub(r"Transcript:.*?Summary:", "", text, flags=re.DOTALL | re.IGNORECASE)
    # remove scale mention like "1 = very inaccurate, 5 = very accurate"
    text = re.sub(r"\b1\s*=\s*[^,.\n]*[,.\n]?\s*5\s*=\s*[^,.\n]*", "", text, flags=re.IGNORECASE)
    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # truncate very long explanations
    if len(text) > max_len:
        text = text[:max_len].rstrip() + " ..."
    return text

# --------------------------
# Batch generation (slice prompt from outputs)
# --------------------------
all_raw = []
n = len(df)
for start in range(0, n, BATCH_SIZE):
    batch_df = df.iloc[start:start + BATCH_SIZE]
    batch_prompts = [
        prompt_template.format(source=row["transcript"], summary=row["lama_summary"])
        for _, row in batch_df.iterrows()
    ]

    inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True).to(device)

    # determine pad id (fallback to eos if pad not defined)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    input_lengths = (inputs["input_ids"] != pad_id).sum(dim=1).tolist()

    with torch.inference_mode():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False
        )

    # per-item: slice off prompt tokens, decode only generated part
    for j, out in enumerate(outputs):
        in_len = input_lengths[j]
        # if output shorter than input (unexpected), decode entire output as fallback
        if out.shape[0] <= in_len:
            gen_tokens = out
        else:
            gen_tokens = out[in_len:]
        decoded = tokenizer.decode(gen_tokens, skip_special_tokens=True)
        all_raw.append(decoded.strip())

# attach raw generation
df["raw_evaluation"] = all_raw

# --------------------------
# Parse and clean results
# --------------------------
ratings = []
explanations = []

for raw in df["raw_evaluation"]:
    rating, explanation = parse_rating_and_explanation(raw)
    explanation = clean_explanation(explanation)
    ratings.append(rating)
    explanations.append(explanation)

df["rating"] = ratings
df["explanation"] = explanations

# debug: print first 3 raw -> parsed so you can verify immediately
for i in range(min(3, len(df))):
    print("---- ROW", i, "----")
    print("RAW OUTPUT:", repr(df.loc[i, "raw_evaluation"])[:400])
    print("PARSED RATING:", df.loc[i, "rating"])
    print("PARSED EXPLANATION:", df.loc[i, "explanation"][:300])
    print()

# --------------------------
# Save results (writable path in pod)
# --------------------------
os.makedirs(BASE_TMP, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print("Saved evaluated CSV to:", OUT_PATH)