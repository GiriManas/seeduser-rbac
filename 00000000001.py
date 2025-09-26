import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "/mnt/nas1/huggingface/Llama-4-Maverick-17B-128E-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

print("Loading model with safe fallback...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",         # spread across GPUs
    offload_folder="offload",  # will store CPU-offloaded tensors here
    local_files_only=True
)

print("✅ Model loaded")

# -------- Test prompt ----------
prompt = "Hello Maverick, how are you?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=64,
        do_sample=False,
        temperature=0.0,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )

decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
print("\n=== Model Output ===")
print(decoded)