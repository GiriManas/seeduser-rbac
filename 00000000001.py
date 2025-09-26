import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "/mnt/nas1/huggingface/Llama-4-Maverick-17B-128E-Instruct"

print("🔹 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

print("🔹 Loading model with device_map + CPU fallback...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    offload_folder="offload",      # CPU fallback
    low_cpu_mem_usage=True,
    local_files_only=True
)

# ---- Fix for meta tensors ----
meta_layers = [name for name, p in model.named_parameters() if p.device.type == "meta"]
if meta_layers:
    print(f"⚠️ Found {len(meta_layers)} meta tensors, offloading them to CPU...")
    for name, param in model.named_parameters():
        if param.device.type == "meta":
            with torch.no_grad():
                new_param = torch.zeros_like(param, device="cpu", dtype=torch.bfloat16)
                param.data = new_param
    print("✅ All meta tensors moved to CPU")

# ---- Tiny test ----
prompt = "Hello Maverick!"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")

print("🚀 Starting generation...")
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=16,
        do_sample=False,
        temperature=0.0,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )

decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\n=== Model Output ===")
print(decoded)