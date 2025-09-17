from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

local_model_path = "./path_to_your_saved_model"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device: {device}")

print("[INFO] Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(local_model_path)

print("[INFO] Loading model in 16-bit (fp16) precision...")

model = AutoModelForCausalLM.from_pretrained(
    local_model_path,
    torch_dtype=torch.float16,   # Force loading in FP16
    device_map="auto",           # Automatically place model on GPU
    max_memory={0: "130GB"}      # Safe limit to avoid hangs
)

print("[INFO] Model loaded successfully in FP16 mode.")

def generate_text(prompt, max_new_tokens=150):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    prompt = "Explain the significance of quantum entanglement."
    print("[INFO] Generating response...")
    output = generate_text(prompt)
    print("\n📝 Generated Output:\n", output)