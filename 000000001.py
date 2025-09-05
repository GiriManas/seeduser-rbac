import os

BASE_TMP = "/tmp/giri/model-test"

# Redirect TorchInductor / Triton / HuggingFace caches
os.environ["TORCHINDUCTOR_CACHE_DIR"] = f"{BASE_TMP}/torchinductor"
os.environ["TRITON_CACHE_DIR"] = f"{BASE_TMP}/triton"
os.environ["HF_HOME"] = f"{BASE_TMP}/huggingface"
os.environ["TRANSFORMERS_CACHE"] = f"{BASE_TMP}/transformers"

# Make sure directories exist
for d in [
    os.environ["TORCHINDUCTOR_CACHE_DIR"],
    os.environ["TRITON_CACHE_DIR"],
    os.environ["HF_HOME"],
    os.environ["TRANSFORMERS_CACHE"],
]:
    os.makedirs(d, exist_ok=True)

# Torch Dynamo fallback (avoids crashing on compilation errors)
import torch
import torch._dynamo as dynamo
dynamo.config.suppress_errors = True

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"  # update if different

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype="auto"
)

prompt = "Write a short story about a scientist who discovers time travel."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("Generating...")
outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.7
)

print("Output:\n", tokenizer.decode(outputs[0], skip_special_tokens=True))