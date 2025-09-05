from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "/mnt/mas1/huggingface/llama-guard-4-12b"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("Model loaded!")

prompt = """<|user|>
Explain how to make a boat.
<|assistant|>"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("Generating...")
outputs = model.generate(**inputs, max_new_tokens=200)

print("Output:\n", tokenizer.decode(outputs[0], skip_special_tokens=True))