from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2.5_3b"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Prepare prompt
prompt = "Explain quantum entanglement in simple terms."

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))