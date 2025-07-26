import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/commons/copra_share/VIPER_NLP/hf_model_hub/phi-3-mini-120k-instruct"

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype=torch.float16
).cuda()

if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

print("Model Loaded.")

prompt = "Write a short poem about the sunrise."

# Tokenize without padding to avoid mismatch
inputs = tokenizer(prompt, return_tensors="pt", padding=False, truncation=True)
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# Ensure attention mask matches input_ids
if "attention_mask" not in inputs:
    inputs["attention_mask"] = torch.ones_like(inputs["input_ids"])

with torch.no_grad():
    output = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )

response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n=== MODEL RESPONSE ===\n")
print(response)