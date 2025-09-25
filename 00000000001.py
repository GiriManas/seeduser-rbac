import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import signal, sys

# ======================
# CONFIG
# ======================
MODEL_PATH = "/mnt/nas1/huggingface/Llama-4-Maverick-17B-128E-Instruct"

print("🔄 Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.bfloat16,
    device_map="auto",           # shard across GPUs
    local_files_only=True
)
print("✅ Model loaded")

# ======================
# Prompt
# ======================
prompt = "Hello Maverick, how are you?"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("\n--- Input Info ---")
print("EOS token id:", tokenizer.eos_token_id)
print("PAD token id:", tokenizer.pad_token_id)
print("Input shape:", inputs["input_ids"].shape)
print("Max position embeddings:", model.config.max_position_embeddings)

# ======================
# Timeout Setup
# ======================
def handler(signum, frame):
    print("\n⏱️ Timeout! Generation took too long, aborting.")
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(120)   # 2 minutes max

# ======================
# Debug: GPU memory before generation
# ======================
if torch.cuda.is_available():
    torch.cuda.synchronize()
    print("\n--- GPU Memory BEFORE ---")
    print(torch.cuda.memory_summary())

# ======================
# Generation
# ======================
print("\n🚀 Starting generation...")
try:
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=16,   # very small for first run
            do_sample=False,
            temperature=0.0,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )
except Exception as e:
    print(f"\n❌ Generation error: {e}")
    sys.exit(1)

signal.alarm(0)   # cancel timeout

# ======================
# Debug: GPU memory after generation
# ======================
if torch.cuda.is_available():
    torch.cuda.synchronize()
    print("\n--- GPU Memory AFTER ---")
    print(torch.cuda.memory_summary())

# ======================
# Decode
# ======================
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
print("\n✅ Model Output:")
print(decoded)