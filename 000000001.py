





outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=max_new_tokens,
    do_sample=True,               # enable sampling
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2,
    no_repeat_ngram_size=3,
    eos_token_id=tokenizer.eos_token_id
)

