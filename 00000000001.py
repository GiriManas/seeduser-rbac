def generate_text(input_prompt):
    # input_prompt can be str or list[str]
    inputs = tokenizer(input_prompt, return_tensors="pt", padding=True, truncation=True).to(device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    # If multiple prompts were given, decode each separately
    decoded = [tokenizer.decode(out, skip_special_tokens=True).strip() for out in outputs]
    
    # Return a string if input was str, else a list
    if isinstance(input_prompt, str):
        return decoded[0]
    else:
        return decoded
        
        
        
        

# Single prompt
print(generate_text("Hello, how are you?"))

# List of prompts
prompts = ["What is AI?", "Explain quantum computing.", "Define gravity."]
responses = generate_text(prompts)

for i, r in zip(prompts, responses):
    print(f"Q: {i}\nA: {r}\n")















<s>[INST] <<SYS>>
You are an evaluator. 
Your task is to assess the completeness of the summary compared to the transcript. 
Completeness means the summary should capture all important information from the transcript.

Return only a rating (digit 1–5) and a short explanation (1–2 sentences). 
Do not repeat transcript or summary. 
Do not output anything else.
<</SYS>>

Transcript:
{source}

Summary:
{summary}

STRICT output format:
Rating: <digit 1-5>
Explanation: <short explanation>
[/INST]

















<s>[INST] <<SYS>>
You are an evaluator. 
Your task is to assess the completeness of the summary compared to the transcript. 
Completeness means the summary should capture all important information from the transcript.

Return only a rating (digit 1–5) and a short explanation (1–2 sentences). 
Do not repeat transcript or summary. 
Do not output anything else.
<</SYS>>

Transcript:
{source}

Summary:
{summary}

STRICT output format:
Rating: <digit 1-5>
Explanation: <short explanation>
[/INST]















llama4_prompt_template = """<s>[INST] <<SYS>>
You are an evaluator.
Your only task is to compare the given summary with the transcript and assign a groundedness rating.
Return strictly in the requested format and nothing else.
Do not generate steps, reasoning, transcripts, or summaries.
Do not include the prompt, input text, or any other explanations.
<</SYS>>

Definition of Groundedness:
Groundedness refers to how well the summary is supported by the content of the transcript.
A grounded summary should accurately reflect the information in the transcript without introducing unsupported claims.

STRICT output format (must follow exactly, no extra words):
Rating: <digit 1-5>
Explanation: <short explanation in one or two sentences>
[/INST]

Transcript:
{source}

Summary:
{summary}
"""













#######################################

<s>[INST] <<SYS>>
You are an evaluator.
Your task is to compare the given summary with the transcript and assign a completeness rating.
Follow the instructions carefully and return output only in the requested format.
Do not include the transcript or summary in your output.
<</SYS>>

Definition of Completeness:
Completeness refers to the extent to which the summary covers all important information from the input context.

STRICT output format (must follow exactly):
Rating: <digit 1-5>
Explanation: <short explanation (one or two sentences)>

Transcript:
{source}

Summary:
{summary}
[/INST]













<s>[INST] <<SYS>>
You are an evaluator.
Your task is to compare the given summary with the transcript and assign a {metric_name} rating.
Follow the instructions carefully and return output only in the requested format.
Do not include the transcript or summary in your output.
<</SYS>>

Definition of {metric_name}:
{metric_definition}

STRICT output format (must follow exactly):
Rating: <digit {rating_scale}>
Explanation: <short explanation (one or two sentences)>

Transcript:
{source}

Summary:
{summary}
[/INST]













######################################





<s>[INST] <<SYS>>
You are an evaluator. 
Return only a rating (digit 1–5) and a short explanation. 
Do not generate steps, transcripts, or summaries. 
Do not include any other text.
<</SYS>>

Transcript:
{source}

Summary:
{summary}

STRICT output format (must follow exactly):
Rating: <digit 1-5>
Explanation: <short explanation, one or two sentences>
[/INST]
















import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# Model path (replace with your actual one)
# --------------------------
MODEL_PATH = "/mnt/nas1/huggingface/llama-4-scout-17b-16e-instruct"

# --------------------------
# Load tokenizer & model
# --------------------------
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)
device = model.device
print("Model loaded on", device)

# --------------------------
# Example input
# --------------------------
transcript = "Agent: Hello, thank you for calling support. How may I help you today?\nCustomer: I want to reset my password."
summary = "The agent greeted the customer and the customer asked to reset their password."

prompt = f"""<s>[INST] <<SYS>>
You are an evaluator. 
Your task is to compare the given summary with the transcript and assign a groundedness rating. 
STRICT output format (must follow exactly):
Rating: <digit 1-5>
Explanation: <short explanation (1–2 sentences)>
<</SYS>>

Transcript:
{transcript}

Summary:
{summary}
[/INST]"""

# --------------------------
# Tokenize & Generate
# --------------------------
inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=False,        # greedy decoding
        temperature=0.0,        # deterministic
        eos_token_id=tokenizer.eos_token_id
    )

decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

print("\n---- RAW OUTPUT ----")
print(decoded)