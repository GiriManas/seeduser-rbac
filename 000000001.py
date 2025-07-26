import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/commons/corpra_share/VIPER_NLP/hf_model_hub/phi-3-mini-120k-instruct"

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

# Tokenize with padding
inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# Prepare inputs for generation (fixing attention mask mismatch)
generation_inputs = model.prepare_inputs_for_generation(inputs["input_ids"], attention_mask=inputs["attention_mask"])

with torch.no_grad():
    output = model.generate(
        **generation_inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id
    )

response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n=== MODEL RESPONSE ===\n")
print(response)