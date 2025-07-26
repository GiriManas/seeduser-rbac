import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/commons/copra_share/VIPER_NLP/hf_model_hub/phi-3-mini-120k-instruct"

print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype=torch.float16
).cuda()

if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

print(f"Tokenizer PAD token ID: {tokenizer.pad_token_id}")
print("Model loaded successfully.")

prompt = "Write a short poem about the sunrise."

# Tokenize WITHOUT padding
inputs = tokenizer(prompt, return_tensors="pt", padding=False, truncation=True)
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# Debugging: Print shapes before generation
print("\n=== DEBUG INPUT SHAPES ===")
for k, v in inputs.items():
    print(f"{k}: {v.shape}")

# Ensure attention mask exists
if "attention_mask" not in inputs:
    inputs["attention_mask"] = torch.ones_like(inputs["input_ids"])
    print("Attention mask was missing; created new mask.")

# Print input values for debugging
print(f"Input IDs: {inputs['input_ids']}")
print(f"Attention Mask: {inputs['attention_mask']}")

print("\n=== GENERATION START ===")

with torch.no_grad():
    try:
        output = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            use_cache=False  # Try disabling cache to avoid shape mismatch
        )
    except Exception as e:
        print(f"\nERROR during generation: {e}")
        raise

response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\n=== MODEL RESPONSE ===")
print(response)