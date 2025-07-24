import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Path to your model directory
model_path = "/commons/copra_share/VIPER_NLP/hf_model_hub/qwen2.5_3b"

# Check GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,   # Use float16 for GPU efficiency
    device_map="auto",           # Automatically select GPU
    trust_remote_code=True
)

# Optional: load generation config if available
try:
    gen_config = GenerationConfig.from_pretrained(model_path)
except:
    gen_config = GenerationConfig()

# Example prompt
prompt = "Explain the importance of GPU acceleration in AI models."

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate output
with torch.no_grad():
    output_ids = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        generation_config=gen_config
    )

# Decode output
response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("\nModel Output:\n", response)