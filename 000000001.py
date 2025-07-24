from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# Set local model directory
model_dir = "/commons/copra_share/VIPER_NLP/hf_model_hub/phi-3-mini-4k-instructs"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

# Load model with half precision, force to GPU
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    trust_remote_code=True,
    torch_dtype=torch.float16
).cuda()  # <== Important: send to CUDA explicitly

# Optional: Load generation config
gen_config = GenerationConfig.from_pretrained(model_dir)

# Set pad token if needed
tokenizer.pad_token = tokenizer.eos_token

# Prompt
prompt = "Explain what is a large language model in simple terms."

# Tokenize input and send tensors to GPU
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# Generate
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        generation_config=gen_config
    )

# Decode
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)