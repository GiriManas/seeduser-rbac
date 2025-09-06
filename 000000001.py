import os
import re
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch._dynamo as dynamo

# ========= TORCH / CACHE FIX =========
BASE_TMP = "/tmp/giri/model-test"

os.environ["TORCHINDUCTOR_CACHE_DIR"] = f"{BASE_TMP}/torchinductor"
os.environ["TRITON_CACHE_DIR"] = f"{BASE_TMP}/triton"
os.environ["XDG_CACHE_HOME"] = f"{BASE_TMP}/xdg"
os.environ["HF_HOME"] = f"{BASE_TMP}/huggingface"
os.environ["TRANSFORMERS_CACHE"] = f"{BASE_TMP}/transformers"

# Fully disable TorchDynamo/Inductor
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["TORCHINDUCTOR_DISABLE"] = "1"

for d in [
    os.environ["TORCHINDUCTOR_CACHE_DIR"],
    os.environ["TRITON_CACHE_DIR"],
    os.environ["XDG_CACHE_HOME"],
    os.environ["HF_HOME"],
    os.environ["TRANSFORMERS_CACHE"],
]:
    os.makedirs(d, exist_ok=True)

# TorchDynamo safety
dynamo.config.suppress_errors = True
torch._dynamo.disable()

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
df = pd.read_csv("your_dataset.csv")  # expects: transcript, lama_summary

prompt_template = """
Evaluate the following summary against the transcript. 
Provide a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate). 
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
            do_sample=False,
            temperature=0.0
        )

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    all_outputs.extend(decoded)

df["raw_evaluation"] = all_outputs

# ========= PARSE RATING + EXPLANATION =========
ratings = []
explanations = []

for text in df["raw_evaluation"]:
    stripped = text.strip()

    # ✅ Only match number at start of output
    match = re.match(r"^\s*([1-5])\s*(?:\n|$)", stripped)
    rating = int(match.group(1)) if match else None

    # ✅ Explanation = everything after rating line
    explanation = ""
    if rating is not None:
        parts = stripped.split("\n", 1)
        if len(parts) > 1:
            explanation = parts[1].strip()

    ratings.append(rating)
    explanations.append(explanation)

df["rating"] = ratings
df["explanation"] = explanations

# ========= CLEANUP =========
def clean_text(t):
    """Remove prompt echoes & tidy spacing."""
    if pd.isna(t):
        return ""
    t = re.sub(r'\s+', ' ', t)  # normalize spaces/newlines
    # Remove any repeated prompt markers
    t = t.replace("Transcript:", "").replace("Summary:", "")
    return t.strip()

df["explanation"] = df["explanation"].apply(clean_text)

# ========= SAVE RESULTS =========
df.to_csv("evaluated_dataset.csv", index=False)

print("🎯 Completed! Results saved to evaluated_dataset.csv")
print(df[["transcript", "lama_summary", "rating", "explanation"]].head())