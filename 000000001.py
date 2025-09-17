from transformers import pipeline
import torch
import os

# ✅ Path to locally saved model (change this path as needed)
local_model_path = "./path_to_your_saved_model"

print("[INFO] Checking GPU availability...")
device = 0 if torch.cuda.is_available() else -1
print(f"[INFO] Inference will run on {'GPU' if device >= 0 else 'CPU'}.")

# ✅ Check that the model directory exists
if not os.path.exists(local_model_path):
    raise FileNotFoundError(f"Model path not found: {local_model_path}")

print("[INFO] Loading pipeline from local folder...")

# ✅ Automatically use quantization if possible
try:
    generator = pipeline(
        task="text-generation",
        model=local_model_path,
        tokenizer=local_model_path,
        device=device,
        load_in_8bit=True   # Automatically fall back if not supported
    )
    print("[INFO] Pipeline loaded in quantized mode (8-bit).")
except Exception as e:
    print(f"[WARNING] Quantized mode not supported: {e}")
    print("[INFO] Falling back to full precision mode.")
    generator = pipeline(
        task="text-generation",
        model=local_model_path,
        tokenizer=local_model_path,
        device=device
    )

print("[INFO] Pipeline is ready for inference.")

# ✅ Example usage function
def generate_text(prompt, max_new_tokens=150):
    result = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )
    return result[0]['generated_text']

# ✅ Example prompt
if __name__ == "__main__":
    prompt = "What are the advantages of electric vehicles?"
    print("[INFO] Generating response...")
    output = generate_text(prompt)
    print("\n📝 Generated Output:\n", output)


















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

