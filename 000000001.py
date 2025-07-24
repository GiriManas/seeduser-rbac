from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# Set local model directory
model_dir = "/commons/copra_share/VIPER_NLP/hf_model_hub/phi-3-mini-4k-instructs"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",         # or device_map={"": "cuda:0"} if needed
    trust_remote_code=True,
    torch_dtype=torch.float16  # Change to float32 if you get any float16 errors
)

# Load generation config (optional)
gen_config = GenerationConfig.from_pretrained(model_dir)

# Prompt
prompt = "Explain what is a large language model in simple terms."

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Generate output
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        generation_config=gen_config
    )

# Decode and print
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)