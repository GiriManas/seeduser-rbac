import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2_5_coder"  # your local path

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)

# Load model on GPU with float16
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map={"": "cuda"},  # Explicitly map to GPU
    trust_remote_code=True,
    local_files_only=True
)

# Prompt and input encoding
prompt = "Write a Python function to check if a number is prime."
inputs = tokenizer(prompt, return_tensors="pt")
inputs = {k: v.to(model.device) for k, v in inputs.items()}  # Move tensors to GPU

# Optional generation config
gen_config = GenerationConfig.from_pretrained(model_path, local_files_only=True)

# Generate output
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        generation_config=gen_config
    )

# Decode and print result
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n=== MODEL OUTPUT ===")
print(response)