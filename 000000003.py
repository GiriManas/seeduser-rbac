import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_qwen_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
    return model, tokenizer

def generate_response(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)

    # Ensure pad_token_id is set
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    model_path = "/your/local/path/to/QwenQwen2.5-3B-Instruct"  # Adjust this
    model, tokenizer = load_qwen_model(model_path)

    prompt = "Explain the significance of photosynthesis."
    response = generate_response(model, tokenizer, prompt)
    print("Response:\n", response)