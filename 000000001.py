
from transformers import pipeline

# ✅ Path to your locally saved model folder
local_model_path = "./path_to_your_saved_model"

print("[INFO] Loading pipeline from local folder with safetensors and multiple shards...")

generator = pipeline(
    task="text-generation",
    model=local_model_path,
    tokenizer=local_model_path,
    device=0,             # Use GPU
    load_in_8bit=True    # Use quantized mode if supported
)

print("[INFO] Pipeline is ready for inference.")

# ✅ Example usage
prompt = "What are the benefits of renewable energy?"
result = generator(prompt, max_new_tokens=150, temperature=0.7, top_k=50, top_p=0.95)

print("\n📝 Generated Output:\n", result[0]['generated_text'])












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

