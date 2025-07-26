from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "/path/to/phi-3-mini-120k-instruct"  # replace with your model dir
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Ensure pad_token_id
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float16
).cuda()

prompt = "Hello, how are you?"
inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)

with torch.no_grad():
    output = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=50,
        pad_token_id=tokenizer.pad_token_id
    )

print(tokenizer.decode(output[0], skip_special_tokens=True))