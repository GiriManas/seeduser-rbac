import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# Load model + tokenizer
# --------------------------
MODEL_PATH = "/mnt/nas1/huggingface/Llama-4-Scout-17B-16E-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)

# --------------------------
# Proper LLaMA-4 prompt format
# --------------------------
prompt = """<s>[INST] <<SYS>>
You are an evaluator. Your task is to rate groundedness.
<</SYS>>

Transcript:
The sky is blue and the sun is shining.

Summary:
The sun is visible.

Give only:
Rating: <digit 1–5>
Explanation: <short explanation> [/INST]"""

# --------------------------
# Tokenize & generate
# --------------------------
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.inference_mode():
    output = model.generate(
        **inputs,
        max_new_tokens=256,   # adjust based on expected output length
        do_sample=False,      # deterministic
        temperature=0.0,
        top_p=1.0
    )

# --------------------------
# Decode cleanly
# --------------------------
# Remove the prompt portion, keep only the new tokens
gen_tokens = output[0][inputs["input_ids"].shape[1]:]
decoded = tokenizer.decode(gen_tokens, skip_special_tokens=True)

print("=== MODEL RESPONSE ===")
print(decoded.strip())