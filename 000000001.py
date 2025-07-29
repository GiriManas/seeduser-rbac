import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the path to your local model directory
model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2.5_3b_vl"  # Update if needed

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).to("cuda")

# Example prompt
prompt = "Explain quantum entanglement in simple terms."

# Tokenize and move inputs to the same device as the model
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Generate output
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )

# Decode and print the result
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)