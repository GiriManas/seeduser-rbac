import os

BASE_TMP = "/tmp/giri/model-test"

# Redirect caches
os.environ["TORCHINDUCTOR_CACHE_DIR"] = f"{BASE_TMP}/torchinductor"
os.environ["TRITON_CACHE_DIR"] = f"{BASE_TMP}/triton"
os.environ["HF_HOME"] = f"{BASE_TMP}/huggingface"
os.environ["TRANSFORMERS_CACHE"] = f"{BASE_TMP}/transformers"

for d in [
    os.environ["TORCHINDUCTOR_CACHE_DIR"],
    os.environ["TRITON_CACHE_DIR"],
    os.environ["HF_HOME"],
    os.environ["TRANSFORMERS_CACHE"],
]:
    os.makedirs(d, exist_ok=True)

import torch
import torch._dynamo as dynamo
dynamo.config.suppress_errors = True

from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_PATH = "/mnt/nas1/huggingface/llama-guard-4-12b"  # adjust to your actual folder

print("Loading Llama Guard...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype="auto"
)

# Example input: text to moderate
prompt = "I hate you! You're terrible."

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model(**inputs)

# Get classification result
predicted_class = torch.argmax(outputs.logits, dim=-1).item()

print("Input:", prompt)
print("Prediction (class ID):", predicted_class)