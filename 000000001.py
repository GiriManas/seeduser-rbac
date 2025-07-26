import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to your local phi-3-mini-120k-instruct folder
MODEL_PATH = "/commons/corpra_share/VIPER_NLP/hf_model_hub/phi-3-mini-120k-instruct"

# Load tokenizer and model
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype=torch.float16
).cuda()

# Make sure pad_token_id is set
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

print("Model Loaded.")

# Test prompt
prompt = "Write a short poem about the sunrise."

# Tokenize with explicit padding
encodings = tokenizer(
    [prompt],
    return_tensors="pt",
    padding=True,
    truncation=True
)

input_ids = encodings["input_ids"].to(model.device)
attention_mask = encodings["attention_mask"].to(model.device)

# Generate output
with torch.no_grad():
    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )

response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n=== MODEL RESPONSE ===\n")
print(response)