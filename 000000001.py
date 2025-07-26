inputs = tokenizer(
    prompt,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=model.config.max_position_embeddings
).to(model.device)

if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

print("Input IDs shape:", inputs["input_ids"].shape)
print("Attention mask shape:", inputs["attention_mask"].shape)
print("Max position embeddings:", model.config.max_position_embeddings)


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
    
    
    
    
