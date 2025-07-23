from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = "/models/qwen-7b-chat"  # change to your actual path

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, device_map="auto")

# Sample prompt
prompt = "你好，请用简单的语言解释什么是量子力学。"  # Example in Chinese, since Qwen is multilingual

# Tokenize and run
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))