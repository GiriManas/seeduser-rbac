import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import pandas as pd
import re

# ----------------------------
# Config
# ----------------------------
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_INPUT_TOKENS = 4000  # keep well within LLaMA context window

# ----------------------------
# Load model & tokenizer
# ----------------------------
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Fix pad token issue for LLaMA
tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
print(f"Model loaded on {DEVICE}")

# ----------------------------
# Prompt template
# ----------------------------
PROMPT_TEMPLATE = """
You are a helpful assistant. Analyze the transcript below and produce a customer service rating
and explanation.

Transcript:
{transcript}

Respond in this JSON format only:
{{
  "rating": <integer between 1 and 5>,
  "explanation": "<short text explanation>"
}}
"""

# ----------------------------
# Parse model output
# ----------------------------
def parse_rating_and_explanation(text):
    rating, explanation = None, None

    try:
        match = re.search(r'"rating"\s*:\s*(\d+)', text)
        if match:
            rating = int(match.group(1))

        match = re.search(r'"explanation"\s*:\s*"(.*?)"', text, re.DOTALL)
        if match:
            explanation = match.group(1).strip()
    except Exception as e:
        print("Parsing error:", e)

    return rating, explanation

# ----------------------------
# Generate with retry
# ----------------------------
def evaluate_record(transcript, retries=2):
    prompt = PROMPT_TEMPLATE.format(transcript=transcript)

    for attempt in range(retries):
        try:
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_INPUT_TOKENS
            ).to(DEVICE)

            # Debug input sizes
            print(f"[DEBUG] tokens={inputs['input_ids'].shape}, non-pad={inputs['attention_mask'].sum().item()}")

            in_len = inputs["input_ids"].shape[1]
            out = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

            # Safe slicing
            if out.shape[1] > in_len:
                gen_tokens = out[:, in_len:]
            else:
                gen_tokens = out

            raw_output = tokenizer.decode(gen_tokens[0], skip_special_tokens=True).strip()
            rating, explanation = parse_rating_and_explanation(raw_output)

            return raw_output, rating, explanation

        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1} failed: {e}")
            if attempt == retries - 1:
                return "", None, ""

    return "", None, ""

# ----------------------------
# Example run
# ----------------------------
if __name__ == "__main__":
    transcripts = [
        "Customer called to report a lost credit card. Agent apologized and explained the reissue process clearly."
    ]

    results = []
    for t in tqdm(transcripts):
        raw, rating, explanation = evaluate_record(t)
        results.append({
            "raw_evaluation": raw,
            "rating": rating,
            "explanation": explanation
        })

    df = pd.DataFrame(results)
    print(df)