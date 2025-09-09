# phi_eval_v1.py
# =====================================================
# Stable v1 evaluation script for Phi with retry logic
# =====================================================

import os
import re
import time
import torch
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

# --------------------------
# ENV + Safety setup
# --------------------------
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["DISABLE_COMPILER"] = "1"   # disable torch compile
torch._dynamo.config.suppress_errors = True
torch._dynamo.config.optimize_ddp = False
torch._dynamo.config.disable = True

# --------------------------
# Model + Tokenizer
# --------------------------
MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"  # update if needed
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
)
model.eval()

# --------------------------
# Prompt Template Builder
# --------------------------
def build_retry_prompt(source, summary, attempt):
    return f"""
You are an evaluator.
Compare the given summary with the transcript and assign a groundedness rating.

STRICT INSTRUCTIONS (Attempt {attempt}):
- The FIRST line must ONLY be the rating (a single digit 1–5).
- Example valid outputs:
  4
  Rating: 3
- After that, write ONLY a short explanation in plain text.
- Do NOT repeat the transcript, summary, or instructions.
- Do NOT output phrases like "Now produce only..." or "required format".
- Any other format is INVALID.

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Parser
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    if not generated_text or not isinstance(generated_text, str):
        return None, None

    s = generated_text.strip()
    s = re.sub(r'^[\s\{\[\"]+|[\s\}\]\"]+$', '', s)
    s = s.replace("**", "").replace("*", "")

    # 1) Match "Rating: 4"
    m = re.search(r"[Rr]ating\s*[:=\-]?\s*([1-5])", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        m2 = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", explanation, re.DOTALL)
        if m2:
            explanation = m2.group(1).strip()
        return rating, explanation

    # 2) Match "Explanation:" first, try to find digit before it
    m = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", s, re.DOTALL)
    if m:
        explanation = m.group(1).strip()
        digit = re.search(r"\b([1-5])\b", s[:m.start()])
        rating = int(digit.group(1)) if digit else None
        return rating, explanation

    # 3) Standalone digit (avoid scale definitions)
    prefix = s[:200]
    for mm in re.finditer(r"\b([1-5])\b", prefix):
        idx_end = mm.end()
        after = s[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):  # skip "1 = very inaccurate"
            continue
        rating = int(mm.group(1))
        explanation = s[idx_end:].strip()
        return rating, explanation

    return None, s.strip()

# --------------------------
# Run model
# --------------------------
def run_model(prompt: str, max_new_tokens=256):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False,
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --------------------------
# Evaluate with retry
# --------------------------
def evaluate_with_retry_phi(row, max_retries=3):
    last_response = None
    for attempt in range(1, max_retries + 1):
        prompt = build_retry_prompt(row["source"], row["summary"], attempt)
        response = run_model(prompt)
        last_response = response

        rating, explanation = parse_rating_and_explanation(response)
        if rating is not None:
            return rating, explanation, response

        print(f"⚠️ Retry {attempt} failed for row -> retrying...")

        time.sleep(0.5)

    return None, None, last_response  # if all retries failed

# --------------------------
# Main Evaluation Loop
# --------------------------
def evaluate_dataset(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)

    for i, row in df.iterrows():
        rating, explanation, raw = evaluate_with_retry_phi(row)
        df.at[i, "raw_output"] = raw
        df.at[i, "rating"] = rating
        df.at[i, "explanation"] = explanation

    df.to_csv(output_csv, index=False)
    print(f"✅ Saved results to {output_csv}")

# --------------------------
# Entry Point
# --------------------------
if __name__ == "__main__":
    evaluate_dataset("input.csv", "phi_eval_results.csv")