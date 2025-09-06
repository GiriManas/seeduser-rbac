import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import pandas as pd

MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16
)

# Example dataframe with transcript+summary
data = [
    {
        "transcript": "customer: welcome to wells fargo ... agent: oh. customer: your call is important...",
        "summary": "agent representative customer why am i being transferred..."
    },
    # add your 200 rows here
]
df = pd.DataFrame(data)

def make_prompt(transcript, summary):
    return f"""
You are a helpful assistant. 
Your job is to rate a summary against the transcript for *groundedness*.

Rules:
- Only output in the format:
<number from 1 to 5>
<one short explanation sentence>

Transcript:
{transcript}

Summary:
{summary}
"""

BATCH_SIZE = 2
all_scores, all_explanations = [], []

for i in range(0, len(df), BATCH_SIZE):
    batch = df.iloc[i:i+BATCH_SIZE]
    prompts = [make_prompt(r["transcript"], r["summary"]) for _, r in batch.iterrows()]

    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            do_sample=False,
            temperature=0.0
        )

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    for text in decoded:
        # Extract score
        match = re.search(r"\b([1-5])\b", text)
        score = int(match.group(1)) if match else None

        # Extract explanation (line after score)
        lines = text.strip().splitlines()
        explanation = None
        if len(lines) > 1:
            explanation = lines[1].strip()

        all_scores.append(score)
        all_explanations.append(explanation)

df["score"] = all_scores
df["explanation"] = all_explanations

print(df.head())