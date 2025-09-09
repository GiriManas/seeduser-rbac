# rating_pipeline_rescue_v1.py
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

# explicitly disable torch dynamo (defensive)
import torch._dynamo as dynamo
dynamo.config.suppress_errors = True
torch._dynamo.disable()

# --------------------------
# CONFIG - edit these
# --------------------------
MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"   # local model path (change as needed)
DATASET_PATH = "your_dataset.csv"                    # CSV path or folder with CSV
OUT_PATH = f"{BASE_TMP}/evaluated_dataset_with_raw.csv"
BATCH_SIZE = 2
MAX_NEW_TOKENS = 256
RESCUE_RETRIES = 3  # try up to 3 times to extract rating from raw output

# Column names (single place to change)
TRANSCRIPT_COL = "transcript"
SUMMARY_COL = "lama_summary"
RAW_COL = "raw_evaluation"           # untouched model output (full decode)
GENERATED_COL = "generated_text"     # the generated portion after prompt (decoded, skip_special_tokens=True)
RATING_COL = "rating"
EXPLANATION_COL = "explanation"

# --------------------------
# Load tokenizer & model (local-only)
# --------------------------
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

# Make sure a pad token exists (many instruct/tokenizers don't set pad)
if tokenizer.pad_token_id is None:
    if tokenizer.eos_token_id is not None:
        # re-use EOS as pad to avoid resizing embeddings
        tokenizer.pad_token = tokenizer.eos_token
        print("Info: tokenizer.pad_token set to eos_token to enable padding.")
    else:
        # add a pad token and resize model embeddings (rare)
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        print("Info: added [PAD] token to tokenizer (will resize embeddings after model load).")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)

# If we added new special tokens above we must resize model embeddings
if tokenizer.pad_token_id is None:
    # This branch shouldn't normally run because we set pad above; just in case:
    model.resize_token_embeddings(len(tokenizer))

device = model.device
print("Model loaded on", device)

# --------------------------
# Read dataset (auto-select csv if given folder)
# --------------------------
if os.path.isdir(DATASET_PATH):
    found = [f for f in os.listdir(DATASET_PATH) if f.lower().endswith(".csv")]
    if not found:
        raise SystemExit(f"No .csv found in directory {DATASET_PATH}. Please supply a file path.")
    DATASET_PATH = os.path.join(DATASET_PATH, found[0])
    print("Auto-selected dataset:", DATASET_PATH)

df = pd.read_csv(DATASET_PATH)
expected_cols = {TRANSCRIPT_COL, SUMMARY_COL}
if not expected_cols.issubset(df.columns):
    raise SystemExit(f"CSV must contain columns: {expected_cols}")

# --------------------------
# Prompt template (single definition)
# --------------------------
prompt_template = """You are an evaluator.
Compare the given summary with the transcript and assign a groundedness rating.

STRICT output format (must follow exactly):
Rating: <digit 1-5>
Explanation: <short explanation (one or two sentences)>

Do NOT repeat the transcript or the summary in your output.

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Robust parser (handles messy outputs)
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    """Return (rating:int|None, explanation:str|None). Works on noisy outputs."""
    if generated_text is None:
        return None, None
    s = generated_text.strip()
    if not s:
        return None, None

    # remove surrounding braces/quotes from JSON-like echoes
    s_clean = re.sub(r'^[\s\{\[\"]+|[\s\}\]\"]+$', '', s).strip()
    s_clean = s_clean.replace("**", "").replace("*", "")

    # 1) "Rating: 4" (case-insensitive)
    m = re.search(r"[Rr]ating\s*[:=\-]?\s*([1-5])\b", s_clean)
    if m:
        rating = int(m.group(1))
        # try to find explanation following "Explanation"
        m2 = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", s_clean[m.end():], re.DOTALL)
        if m2:
            explanation = m2.group(1).strip()
        else:
            # take remainder after rating as explanation
            explanation = s_clean[m.end():].strip()
        return rating, explanation or None

    # 2) digit on first line, e.g. "4\nExplanation: ..." or "4\nsomething"
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s_clean)
    if m:
        rating = int(m.group(1))
        explanation = s_clean[m.end():].strip()
        return rating, explanation or None

    # 3) "4/5" near start
    m = re.search(r"\b([1-5])\s*/\s*5\b", s_clean)
    if m:
        rating = int(m.group(1))
        explanation = s_clean[m.end():].strip()
        return rating, explanation or None

    # 4) Fallback: first digit 1-5 in early text but avoid scale definitions "1 = very..."
    prefix = s_clean[:300]
    for mm in re.finditer(r"\b([1-5])\b", prefix):
        idx_end = mm.end()
        after = s_clean[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):  # skip scale defs like "1 = very..."
            continue
        rating = int(mm.group(1))
        explanation = s_clean[idx_end:].strip()
        return rating, explanation or None

    # 5) nothing found
    return None, s_clean or None

def clean_explanation(text: str, max_len: int = 800):
    if not text:
        return ""
    t = text
    t = re.sub(r"Transcript:.*?Summary:", "", t, flags=re.DOTALL | re.IGNORECASE)
    # remove scale mention like "1 = very inaccurate, 5 = very accurate"
    t = re.sub(r"\b1\s*=\s*[^,.\n]*[,.\n]?\s*5\s*=\s*[^,.\n]*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > max_len:
        t = t[:max_len].rstrip() + " ..."
    return t

# --------------------------
# Helper: run generation for a list of prompts, return outputs (full decode)
# --------------------------
def generate_full_outputs(prompts, max_new_tokens=MAX_NEW_TOKENS):
    """
    prompts: list[str]
    returns: list[str] full decoded outputs (model's response INCLUDING prompt echo if present)
    """
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(device)

    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    input_lengths = (inputs["input_ids"] != pad_id).sum(dim=1).tolist()

    with torch.inference_mode():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

    decoded_full = []
    decoded_generated = []
    for i, out in enumerate(outputs):
        # out is a tensor of token ids (input + generated). We decode full to preserve "untouched" output.
        full_text = tokenizer.decode(out, skip_special_tokens=False)  # keep raw tokens as-is
        # generated-only slice (after input length)
        in_len = input_lengths[i]
        if out.shape[0] > in_len:
            gen_tokens = out[in_len:]
            gen_text = tokenizer.decode(gen_tokens, skip_special_tokens=True)
        else:
            gen_text = ""  # model didn't emit new tokens beyond the input
        decoded_full.append(full_text)
        decoded_generated.append(gen_text)
    return decoded_full, decoded_generated

# --------------------------
# Main loop: batch -> generate -> parse -> rescue if needed
# --------------------------
all_raw = []
all_generated = []
all_ratings = []
all_explanations = []

n = len(df)
print("Total records:", n)

for start in range(0, n, BATCH_SIZE):
    batch_df = df.iloc[start : start + BATCH_SIZE]
    prompts = [
        prompt_template.format(source=row[TRANSCRIPT_COL], summary=row[SUMMARY_COL])
        for _, row in batch_df.iterrows()
    ]

    try:
        full_outs, gen_outs = generate_full_outputs(prompts, max_new_tokens=MAX_NEW_TOKENS)
    except Exception as exc:
        # if generation failed for the batch, fail gracefully with debug info
        print(f"Generation error on batch starting at {start}: {exc}")
        # fill placeholders and continue
        for _ in range(len(prompts)):
            all_raw.append("")
            all_generated.append("")
            all_ratings.append(None)
            all_explanations.append("")
        continue

    # per-item parse & rescue
    for idx_in_batch, (raw_full, gen_text) in enumerate(zip(full_outs, gen_outs)):
        all_raw.append(raw_full)         # untouched full decode
        all_generated.append(gen_text)   # generated portion (may be empty)

        # 1) Try parse from raw_full
        rating, explanation = parse_rating_and_explanation(raw_full)

        # 2) If no rating found, try parse from generated-only text (less noisy)
        if rating is None and gen_text:
            rating, explanation = parse_rating_and_explanation(gen_text)

        # 3) If still None, attempt rescue: ask model (up to RESCUE_RETRIES)
        rescue_attempt = 0
        rescue_success = False
        while rating is None and rescue_attempt < RESCUE_RETRIES:
            rescue_attempt += 1
            rescue_prompt = (
                "You will be given a TEXT blob that is the raw output of a model. "
                "Extract ONLY the rating (a single digit 1-5) and a one-line explanation. "
                "Output MUST be exactly in this strict format (no extra text):\n\n"
                "Rating: <digit 1-5>\n"
                "Explanation: <short explanation>\n\n"
                "TEXT:\n"
                f"{raw_full}\n\n"
                "If no valid rating can be found, output 'Rating: NONE' on the first line and a short reason on the second line."
            )
            # tokenize & generate (single prompt)
            try:
                rescue_inputs = tokenizer(rescue_prompt, return_tensors="pt", truncation=True).to(device)
                with torch.inference_mode():
                    rescue_out = model.generate(
                        input_ids=rescue_inputs["input_ids"],
                        attention_mask=rescue_inputs.get("attention_mask", None),
                        max_new_tokens=32,
                        do_sample=False
                    )
                rescue_decoded = tokenizer.decode(rescue_out[0], skip_special_tokens=True).strip()
            except Exception as e:
                print(f"Rescue generation failed (attempt {rescue_attempt}) for row {start + idx_in_batch}: {e}")
                rescue_decoded = ""

            # try parse rescue_decoded
            r2, e2 = parse_rating_and_explanation(rescue_decoded)
            if r2 is None:
                # also accept explicit "Rating: NONE" -> set rating None but explanation from model
                if rescue_decoded and "Rating" in rescue_decoded and "NONE" in rescue_decoded.upper():
                    # set rating None but keep explanation
                    rating = None
                    explanation = rescue_decoded
                    rescue_success = True
                    break
                # else continue retrying
                rating = None
                explanation = e2 or explanation
            else:
                rating = r2
                explanation = e2 or explanation
                rescue_success = True
                break

        # final cleaning
        final_explanation = clean_explanation(explanation)
        all_ratings.append(rating)
        all_explanations.append(final_explanation)

# attach to dataframe
df[RAW_COL] = all_raw
df[GENERATED_COL] = all_generated
df[RATING_COL] = all_ratings
df[EXPLANATION_COL] = all_explanations

# --------------------------
# Debugging summary & save
# --------------------------
num_parsed = df[RATING_COL].notna().sum()
num_total = len(df)
num_none = num_total - num_parsed
print(f"\nParsed ratings: {num_parsed}/{num_total}. Missing: {num_none}")

if num_none > 0:
    print("Indices with missing rating (first 50):", df[df[RATING_COL].isna()].index.tolist()[:50])

# ensure out dir exists
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print("Saved evaluated CSV to:", OUT_PATH)

# Print first few rows for quick verification
print(df[[TRANSCRIPT_COL, SUMMARY_COL, RAW_COL, GENERATED_COL, RATING_COL, EXPLANATION_COL]].head(6))