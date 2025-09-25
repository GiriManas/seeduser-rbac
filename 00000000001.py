import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "/mnt/nas1/huggingface/Llama-4-Maverick-17B-128E-Instruct"

print("🔹 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

print("🔹 Loading model with auto device map + offloading...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",             # spread across GPUs
    offload_folder="offload",      # fallback to CPU if needed
    low_cpu_mem_usage=True,
    local_files_only=True
)
print("✅ Model loaded")

# ---- Check for meta tensors ----
print("🔍 Checking parameter devices...")
meta_layers = [name for name, p in model.named_parameters() if p.device.type == "meta"]
if meta_layers:
    print("⚠️ Still on meta:", meta_layers[:5], "...")
else:
    print("✅ All params correctly placed")

# ---- Tiny test ----
prompt = "Hello Maverick!"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")  # send input only to GPU0

print("🚀 Starting generation...")
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=16,          # very small for test
        do_sample=False,
        temperature=0.0,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )

decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\n=== Model Output ===")
print(decoded)