from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Model name
MODEL_NAME = "google/gemma-3-27b-it"

# Load tokenizer & model
print("Loading model... this may take a while.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,  # efficient with big models
    device_map="auto"            # spread across your 2 GPUs
)

# Example prompt
prompt = "Explain the importance of FastAPI for serving large language models in production."

# Tokenize
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# Generate output
outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    temperature=0.7,
    do_sample=True
)

# Decode & print
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\n=== Model Output ===\n")
print(result)