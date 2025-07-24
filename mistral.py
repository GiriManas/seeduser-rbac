from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = "/path/to/your/local/mistral-7b"  # folder with config.json, tokenizer.json, model.safetensors or .bin

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, device_map="auto").eval()

prompt = "How are you?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))