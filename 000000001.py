import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ========= CACHE FIX =========
BASE_TMP = "/tmp/giri/model-test"

os.environ["TORCHINDUCTOR_CACHE_DIR"] = f"{BASE_TMP}/torchinductor"
os.environ["TRITON_CACHE_DIR"] = f"{BASE_TMP}/triton"
os.environ["XDG_CACHE_HOME"] = f"{BASE_TMP}/xdg"
os.environ["HF_HOME"] = f"{BASE_TMP}/huggingface"
os.environ["TRANSFORMERS_CACHE"] = f"{BASE_TMP}/transformers"

for d in [
    os.environ["TORCHINDUCTOR_CACHE_DIR"],
    os.environ["TRITON_CACHE_DIR"],
    os.environ["XDG_CACHE_HOME"],
    os.environ["HF_HOME"],
    os.environ["TRANSFORMERS_CACHE"],
]:
    os.makedirs(d, exist_ok=True)

# ========= TORCH DYNAMO SAFETY =========
import torch._dynamo as dynamo
dynamo.config.suppress_errors = True
torch._dynamo.disable()   # disables inductor if it fails

# ========= MODEL LOADING =========
MODEL_PATH = "/mnt/nas1/huggingface/gemma-3-27b-it"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16
)
print("Model loaded!")

# ========= PROMPTS (replace with your dataset) =========
prompts = [
    """Evaluate this summary:

    Transcript: customer: welcome to wells fargo ... agent: oh. customer: your call is important...
    Summary: agent representative customer why am i being transferred...

    Provide a score from 1–5 for groundedness (accuracy to transcript).
    Output format:
    [number]
    [explanation]
    """,

    "Summarize Hamlet in one sentence and rate summary groundedness from 1–5.\nTranscript: Hamlet story...",
    # ... load your 200 prompts here (e.g. from pandas DataFrame)
]

# ========= BATCH GENERATION =========
BATCH_SIZE = 2  # tune based on GPU memory
all_outputs = []

for i in range(0, len(prompts), BATCH_SIZE):
    batch_prompts = prompts[i:i+BATCH_SIZE]

    inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7
        )

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    all_outputs.extend(decoded)

# ========= SHOW SAMPLE OUTPUTS =========
print("\n=== Example Outputs ===")
for i, out in enumerate(all_outputs[:5]):
    print(f"\nPrompt {i+1} Output:\n{out}\n")