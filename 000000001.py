import os
import re
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

# ========= FULLY DISABLE TORCHDYNAMO/INDUCTOR =========
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["TORCHINDUCTOR_DISABLE"] = "1"

import torch._dynamo as dynamo
dynamo.config.suppress_errors = True
torch._dynamo.disable()

# ========= CACHE FIX (CUSTOM CACHE DIRS) =========
BASE_TMP = "/tmp/giri/model-test"
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

# ========= MODEL LOADING =========
MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"
print("Loading model and tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16
)
print("✅ Model loaded!")

# ========= LOAD DATA =========
df = pd.read_csv("your_dataset.csv")  # replace with your dataset
# Must have: transcript, lama_summary columns

prompt_template = """
Evaluate the following summary against the transcript.
Give a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate).
Then provide a short explanation.

Output format:
[number]
[explanation]

Transcript:
{source}

Summary:
{output}
"""

# ========= BATCH PROCESSING =========
BATCH_SIZE = 2
all_outputs = []

messages = [
    prompt_template.format(source=row["transcript"], output=row["lama_summary"])
    for _, row in df.iterrows()
]

for i in range(0, len(messages), BATCH_SIZE):
    batch_prompts = messages[i:i+BATCH_SIZE]

    inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False
        )

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    all_outputs.extend(decoded)

df["raw_evaluation"] = all_outputs

# ========= PARSE RATING + EXPLANATION =========
ratings, explanations = [], []

for text in df["raw_evaluation"]:
    match = re.search(r"\b([1-5])\b", text)
    rating = int(match.group(1)) if match else None

    if rating is not None:
        # remove only the first occurrence of the rating
        explanation = text.split(str(rating), 1)[-1].strip()
    else:
        explanation = text.strip()

    ratings.append(rating)
    explanations.append(explanation)

df["rating"] = ratings
df["explanation"] = explanations

# ========= SAVE RESULTS =========
out_path = "evaluated_dataset.csv"
df.to_csv(out_path, index=False)

print(f"🎯 Completed! Results saved to {out_path}")
print(df[["transcript", "lama_summary", "rating", "explanation"]].head())