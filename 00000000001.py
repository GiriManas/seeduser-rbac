import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "/path/to/llama-4-scout-17b-instruct"  # update with your local path



model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,   # safer for big models
    device_map="auto",            # uses GPU automatically
    attn_implementation="flash_attention_2",  # faster + longer context
)


tokenizer = AutoTokenizer.from_pretrained(model_path)


prompt = """
You are an expert summarizer. Summarize the following transcript clearly:

[INSERT LONG TRANSCRIPT HERE]
"""

inputs = tokenizer(
    prompt,
    return_tensors="pt",
    truncation=False  # allow long transcripts
).to("cuda" if torch.cuda.is_available() else "cpu")



output = model.generate(
    **inputs,
    max_new_tokens=2048,     # how much new text to generate
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    repetition_penalty=1.1,
    eos_token_id=tokenizer.eos_token_id,
)


response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)





