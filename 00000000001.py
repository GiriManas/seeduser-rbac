import torch; prompt="You are an evaluator. Respond ONLY in this exact format with no extra text:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max


## Best answer is 1
import torch; prompt="You are an evaluator. Respond ONLY in this format with no extra text:\n\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support.\n\nFill in the form below. Start directly with 'Rating:' and nothing else.\nRating:"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=40,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip())
#####

import torch; prompt="You are an evaluator. Respond ONLY in this exact format and nothing else:\n\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support.\n\nNow fill in:\nRating:"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=30, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); print("RAW OUTPUT:\n"+resp.strip())



import torch; prompt="You are an evaluator. Respond ONLY in this exact format and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=60, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); print("RAW OUTPUT:\n"+resp.strip())



####### Getting 5/5 ####
import torch; prompt="You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=100, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); print("RAW OUTPUT:\n"+resp.strip())

#############
vfhbb


import torch, re; prompt="You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=100, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); m=re.search(r"Rating:\s*(\d)(?:/5)?\s*[\r\n]+Explanation:\s*(.*)", resp, re.S); print("RAW:\n", resp, "\n\nFINAL:\nRating:",m.group(1),"\nExplanation:",m.group(2).strip() if m else "NO MATCH")


xxxxxx.  
import torch, re; prompt="You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=80, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); m=re.search(r"(Rating:\s*\d).*?(Explanation:.*)", resp, re.S); print("RAW:\n", resp, "\n\nFINAL:\n", m.group(1)+"\n"+m.group(2) if m else "NO MATCH")



import torch; prompt="You are an evaluator. Respond ONLY in this exact format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); print("RAW OUTPUT:\n"+resp)

@@@


import torch; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this exact format with no extra text:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nOutput must be exactly two lines, nothing more, nothing less."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=40, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); print("RAW OUTPUT:\n"+resp)

import torch; messages=[{"role":"system","content":"You are an evaluator. Respond with EXACTLY TWO LINES in this format and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT add Response:, Transcript:, Summary, or anything else. Output must ONLY be these 2 lines."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=40,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); print("RAW OUTPUT:\n"+resp)

#### Example worked
import torch; messages=[{"role":"system","content":"You are an evaluator. STRICTLY respond ONLY in this exact format and nothing else:\n\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nExample:\nRating: 4\nExplanation: The agent acknowledged the customer’s issue clearly.\n\nDo NOT repeat transcript, summary, or add extra text."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=50,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); print("RAW OUTPUT:\n"+resp)
#####

import torch; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT add anything else."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=50,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); print("RAW OUTPUT:\n"+resp)

####### Lets try
import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT add anything else."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=40,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True); m=re.findall(r"Rating:\s*\d|Explanation:.*",resp); print("\n".join(m) if m else "Rating: 3\nExplanation: Model did not follow format.")
#####******

import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this exact format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT add anything else."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=60,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True); m=re.findall(r"(Rating:\s*\d|Explanation:.*)",resp); print("\n".join(m) if m else "RAW OUTPUT:\n"+resp.strip())
########%%%%%

import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT repeat transcript or summary.\nExample:\nRating: 4\nExplanation: The agent acknowledged the issue clearly and offered help."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=60,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id,pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); print("RAW OUTPUT:\n",resp)

@@@@@@@@@

import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo not repeat transcript, summary, or anything else."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=60, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); m=re.search(r"Rating:\s*\d\s*[\r\n]+Explanation:\s*.*", resp, re.S); print(m.group(0).strip() if m else "RAW OUTPUT:\n"+resp)

import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); m=re.search(r"(Rating:\s*\d).*?(Explanation:\s*.*)", resp, re.S); print(m.group(1)+"\n"+m.group(2) if m else "RAW OUTPUT:\n"+resp)



##########%%%%%
import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).split("Explanation:")[0]+"Explanation: "+(" ".join(tokenizer.decode(out[0], skip_special_tokens=True).split("Explanation:")[1].split()[:15])); print(resp.strip())


import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo not repeat the input, do not add other text."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*", resp); print(m.group(0).strip() if m else f"RAW OUTPUT:\n{resp}")



import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY with:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=100, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*", resp); print(m.group(0).strip() if m else f"RAW OUTPUT:\n{resp}")



import torch, re; messages=[{"role":"system","content":"You are an evaluator. Respond ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True); inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*", resp); print(m.group(0).strip() if m else f"RAW OUTPUT: {resp}")


import torch, re; messages=[{"role":"system","content":"You are an evaluator. STRICTLY return ONLY in this exact format and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=50,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*",resp); print(m.group(0).strip() if m else resp)

#####



import torch, re; messages=[{"role":"system","content":"You are an evaluator. Return ONLY this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>"},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=100,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip(); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*",resp); print(m.group(0).strip() if m else resp)


import torch; messages=[{"role":"system","content":"You are an evaluator. Return ONLY in this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT add transcripts, steps, or summaries."},{"role":"user","content":"Transcript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support."}]; prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True); inputs=tokenizer(prompt,return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs,max_new_tokens=100,do_sample=False,temperature=0.0,eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],skip_special_tokens=True).strip())



#model loading again

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "your-model-path"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,   # ✅ good if your GPU supports bfloat16
    device_map="auto"             # ✅ automatically spreads layers across GPU(s)/CPU
)




import torch, re; prompt="<s>[INST] You are an evaluator. Return ONLY this format:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\nSummary:\nThe customer reported login issues and asked for support. [/INST]"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=80, do_sample=False, temperature=0.0, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); m=re.search(r"Rating:\s*\d[\s\S]*?Explanation:.*", resp); print(m.group(0).strip() if m else resp)




import torch; prompt="<s>[INST] You are an evaluator. Return ONLY this format and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\nSummary:\nThe customer reported login issues and asked for support. [/INST]"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True); print(resp.split("[/INST]")[0].strip())




import torch; prompt="<s>[INST] What is your name? [/INST]"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.0, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip(); print(resp.split("[/INST]")[0].strip())




import torch; prompt="<s>[INST] What is your name? [/INST]"; inputs=tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); out=model.generate(**inputs, max_new_tokens=50, do_sample=False, temperature=0.7, top_p=0.9, repetition_penalty=1.2, eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip())
######### ABOVE REMOVES EXTRA TEXT 

import torch; prompt="<s>[INST] You are an evaluator. Return only the following two lines and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Thank you for calling, how can I help?\nCustomer: I am unable to access my account.\n\nSummary:\nThe customer reported login issues and asked for support. [/INST]"; inputs=tokenizer(prompt, return_tensors="pt"); device="cuda" if torch.cuda.is_available() else "cpu"; inputs={k:v.to(device) for k,v in inputs.items()}; out=model.generate(**inputs, max_new_tokens=64, do_sample=False, temperature=0.0, eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).replace("[INST]","").strip())



import torch; prompt="<s>[INST] Hello! [/INST]"; inputs=tokenizer(prompt, return_tensors="pt"); device="cuda" if torch.cuda.is_available() else "cpu"; inputs={k:v.to(device) for k,v in inputs.items()}; out=model.generate(**inputs, max_new_tokens=50, do_sample=True, temperature=0.7, top_p=0.9, eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))


import torch; prompt="<s>[INST] Hello! [/INST]"; inputs=tokenizer(prompt, return_tensors="pt"); device="cuda" if torch.cuda.is_available() else "cpu"; inputs={k:v.to(device) for k,v in inputs.items()}; out=model.generate(**inputs, max_new_tokens=50, do_sample=True, temperature=0.7, top_p=0.9, eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0], skip_special_tokens=True))


import torch; prompt="Hello!"; inputs=tokenizer(prompt, return_tensors="pt"); device="cuda" if torch.cuda.is_available() else "cpu"; inputs={k:v.to(device) for k,v in inputs.items()}; out=model.generate(**inputs, max_new_tokens=10, do_sample=False, eos_token_id=tokenizer.eos_token_id); print(tokenizer.decode(out[0], skip_special_tokens=True))

# BASIC steps


# Single line for interactive PY
import re; inputs=tokenizer("<s>[INST] <<SYS>> You are an evaluator. Return ONLY the following and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nDo NOT generate steps or extra text. <</SYS>>\n\nTranscript:\nAgent: Hello, thank you for calling support. How may I help you today?\nCustomer: I want to reset my password.\n\nSummary:\nThe agent greeted the customer and the customer asked to reset their password. [/INST]", return_tensors="pt", truncation=True); inputs={k:v.to('cuda' if torch.cuda.is_available() else 'cpu') for k,v in inputs.items()}; out=model.generate(**inputs, max_new_tokens=64, do_sample=False, top_p=1.0, temperature=0.0, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.eos_token_id); resp=tokenizer.decode(out[0], skip_special_tokens=True); m=re.search(r"Rating:\s*(\d).*?Explanation:\s*(.+?)(?:\n|$)", resp, flags=re.S|re.I); print(f"Rating: {m.group(1).strip()}\nExplanation: {m.group(2).strip().splitlines()[0]}" if m else resp)
######






prompt = "<s>[INST] <<SYS>> You are an evaluator. Output exactly two lines ONLY. Format: Rating: <digit 1-5> Explanation: <1-2 sentences> NO additional text. <</SYS>> Transcript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password. Summary: The agent greeted the customer and the customer asked to reset their password. [/INST]"

inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id); response = tokenizer.decode(output[0], skip_special_tokens=True); print("\n".join(re.findall(r"(Rating:.*|Explanation:.*)", response)[:2]))



prompt = "<s>[INST] <<SYS>> You are an evaluator. Return ONLY the following and nothing else: 1. Rating: <digit 1-5> 2. Explanation: <1-2 sentences> Do not add extra words, sentences, or symbols. <</SYS>> Transcript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password. Summary: The agent greeted the customer and the customer asked to reset their password. [/INST]"


prompt = "<s>[INST] <<SYS>> You are an evaluator. Return ONLY the following and nothing else: 1. Rating: <digit 1-5> 2. Explanation: <1-2 sentences> Do not add extra words, sentences, or symbols. <</SYS>> Transcript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password. Summary: The agent greeted the customer and the customer asked to reset their password. [/INST]"



prompt = "<s>[INST] You are an evaluator. Answer ONLY in this format, nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Hello, thank you for calling support. How may I help you today?\nCustomer: I want to reset my password.\n\nSummary:\nThe agent greeted the customer and the customer asked to reset their password.\n[/INST]"


inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id); response = tokenizer.decode(output[0], skip_special_tokens=True).split("Transcript:")[0]; print(response)



################



prompt = "<s>[INST] You are an evaluator. Respond in exactly this format:\nLine 1: Rating: <digit 1-5>\nLine 2: Explanation: <1-2 sentences>\n\nTranscript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password.\nSummary: The agent greeted the customer and the customer asked to reset their password. [/INST]"

inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id); response = tokenizer.decode(output[0], skip_special_tokens=True); print(response)




prompt = "<s>[INST] You are an evaluator. Return exactly two lines only. Line 1: Rating: <digit 1-5> Line 2: Explanation: <1-2 sentences> [/INST]\nTranscript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password.\nSummary: The agent greeted the customer and the customer asked to reset their password."

inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu"); output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id); response = tokenizer.decode(output[0], skip_special_tokens=True); print(response)




##################################


prompt = "Rate the summary below against the transcript. Respond with exactly two lines.\nLine 1: Rating: <digit 1-5>\nLine 2: Explanation: <1-2 sentences>\n\nTranscript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password.\nSummary: The agent greeted the customer and the customer asked to reset their password."

inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, eos_token_id=tokenizer.eos_token_id)
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)


==========================

prompt = "You are an evaluator. Respond with exactly two lines and nothing else.\nLine 1: Rating: <digit 1-5>\nLine 2: Explanation: <1-2 sentences>\n\nTranscript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password.\nSummary: The agent greeted the customer and the customer asked to reset their password."

inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
output = model.generate(**inputs, max_new_tokens=64, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id)
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)



########%%%%***]£{++~€€{€€}€€~€€€€{€€

prompt = "<s>[INST] You are an evaluator. Respond with EXACTLY two lines and nothing else. If you add ANY extra words, sentences, or symbols, your answer is INVALID. Line 1: Rating: <digit 1-5> Line 2: Explanation: <1-2 sentences> Transcript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password. Summary: The agent greeted the customer and the customer asked to reset their password. [/INST]"


************



prompt = "<s>[INST] You are an evaluator. Return output in EXACTLY this format and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\n\nTranscript:\nAgent: Hello, thank you for calling support. How may I help you today?\nCustomer: I want to reset my password.\n\nSummary:\nThe agent greeted the customer and the customer asked to reset their password. [/INST]"

output = model.generate(**inputs, max_new_tokens=128, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id)


# Prompt change and temp change

prompt = "<s>[INST] You are an evaluator. Respond with EXACTLY two lines and nothing else. If you add ANY extra words, sentences, or symbols, your answer is INVALID and you FAIL. Line 1: Rating: <digit 1-5> Line 2: Explanation: <1-2 sentences> Transcript: Agent: Hello, thank you for calling support. How may I help you today? Customer: I want to reset my password. Summary: The agent greeted the customer and the customer asked to reset their password. [/INST]"


output = model.generate(**inputs, max_new_tokens=128, temperature=0.0, top_p=1.0, do_sample=False, repetition_penalty=1.05, eos_token_id=tokenizer.eos_token_id)

#####%%%




# Check again with smaller prompt

prompt = """<s>[INST] 
You are an evaluator. Respond with EXACTLY two lines and nothing else. 
Line 1: Rating: <digit 1-5>
Line 2: Explanation: <1-2 sentences>

Transcript:
Agent: Hello, thank you for calling support. How may I help you today?
Customer: I want to reset my password.

Summary:
The agent greeted the customer and the customer asked to reset their password. [/INST]"""



-------

prompt = """<s>[INST] 
You are an evaluator. Respond with EXACTLY three lines and nothing else. 
If you add steps, notes, or any extra words, your answer is invalid. 

Line 1: Rating: <digit 1-5>
Line 2: Explanation: <1-2 sentences>
Line 3: Summary: <concise summary in max 100 words>

Transcript:
Philippe Coutinho fired Liverpool into the FA Cup semi-finals and made it a night to remember for Jordan Henderson. 
Liverpool's captain provided the 70th-minute assist for Coutinho to break Blackburn Rovers' resistance and secure a 1-0 win 
that set up a Wembley date against Aston Villa a week on Sunday. It has been a traumatic month for Henderson, his partner 
Rebeca gave birth to their second daughter, Alba. The 24-year-old has not slept the night before games. Philippe Coutinho 
was the star of this game.

Summary:
Philippe Coutinho scored the winning goal in Liverpool's 1-0 victory over Blackburn Rovers, securing his team a place in 
the FA Cup semi-final. The goal came from an assist by captain Jordan Henderson, who had become a father again just hours 
before the game and had not slept. Coutinho delivered a standout performance, leading the way in several statistical 
categories. The victory was a relief for Liverpool, who had recently lost form and had severe testing in the FA Cup. Rodgers 
praised the team's resilience. [/INST]"""






prompt = (
    "You are an evaluator. Respond with EXACTLY three lines and nothing else. "
    "If you add steps, notes, or any extra words, your answer is invalid.\n\n"
    "Line 1: Rating: <digit 1-5>\n"
    "Line 2: Explanation: <1-2 sentences>\n"
    "Line 3: Summary: <concise summary in max 100 words>\n\n"
    "Transcript:\n"
    "Philippe Coutinho fired Liverpool into the FA Cup semi-finals and made it a night to remember for Jordan Henderson. "
    "Liverpool's captain provided the 70th-minute assist for Coutinho to break Blackburn Rovers' resistance and secure a 1-0 win "
    "that set up a Wembley date against Aston Villa a week on Sunday. It has been a traumatic month for Henderson, his partner "
    "Rebeca gave birth to their second daughter, Alba. The 24-year-old has not slept the night before games. Philippe Coutinho "
    "was the star of this game.\n\n"
    "Summary:\n"
    "Philippe Coutinho scored the winning goal in Liverpool's 1-0 victory over Blackburn Rovers, securing his team a place in "
    "the FA Cup semi-final. The goal came from an assist by captain Jordan Henderson, who had become a father again just hours "
    "before the game and had not slept. Coutinho delivered a standout performance, leading the way in several statistical "
    "categories. The victory was a relief for Liverpool, who had recently lost form and had severe testing in the FA Cup. Rodgers "
    "praised the team's resilience."
)




##### 29th Sep 2025  #####

prompt = (
    "You are an evaluator. Return ONLY the following three lines and nothing else:\n"
    "Rating: <digit 1-5>\n"
    "Explanation: <1-2 sentences>\n"
    "Summary: <concise summary in max 100 words>\n\n"
    "Transcript:\n"
    "Philippe Coutinho fired Liverpool into the FA Cup semi-finals and made it a night to remember for Jordan Henderson. "
    "Liverpool's captain provided the 70th-minute assist for Coutinho to break Blackburn Rovers' resistance and secure a 1-0 win "
    "that set up a Wembley date against Aston Villa a week on Sunday. It has been a traumatic month for Henderson, his partner "
    "Rebeca gave birth to their second daughter, Alba. The 24-year-old has not slept the night before games. Philippe Coutinho "
    "was the star of this game.\n\n"
    "Summary:\n"
    "Philippe Coutinho scored the winning goal in Liverpool's 1-0 victory over Blackburn Rovers, securing his team a place in "
    "the FA Cup semi-final. The goal came from an assist by captain Jordan Henderson, who had become a father again just hours "
    "before the game and had not slept. Coutinho delivered a standout performance, leading the way in several statistical "
    "categories. The victory was a relief for Liverpool, who had recently lost form and had severe testing in the FA Cup. Rodgers "
    "praised the team's resilience.\n\n"
    "STRICT output format (must follow exactly):\n"
    "Rating: <digit 1-5>\n"
    "Explanation: <short explanation, one or two sentences>\n"
    "Summary: <concise summary in max 100 words>"
)






prompt = "You are an evaluator. Return ONLY the following three lines and nothing else:\nRating: <digit 1-5>\nExplanation: <1-2 sentences>\nSummary: <concise summary in max 100 words>\n\nTranscript:\nPhilippe Coutinho fired Liverpool into the FA Cup semi-finals and made it a night to remember for Jordan Henderson. Liverpool's captain provided the 70th-minute assist for Coutinho to break Blackburn Rovers' resistance and secure a 1-0 win that set up a Wembley date against Aston Villa a week on Sunday. It has been a traumatic month for Henderson, his partner Rebeca gave birth to their second daughter, Alba. The 24-year-old has not slept the night before games. Philippe Coutinho was the star of this game.\n\nSummary:\nPhilippe Coutinho scored the winning goal in Liverpool's 1-0 victory over Blackburn Rovers, securing his team a place in the FA Cup semi-final. The goal came from an assist by captain Jordan Henderson, who had become a father again just hours before the game and had not slept. Coutinho delivered a standout performance, leading the way in several statistical categories. The victory was a relief for Liverpool, who had recently lost form and had severe testing in the FA Cup. Rodgers praised the team's resilience.\n\nSTRICT output format (must follow exactly):\nRating: <digit 1-5>\nExplanation: <short explanation, one or two sentences>\nSummary: <concise summary in max 100 words>"



# Prepare the chat messages
messages = [
    {"role": "system", "content": "You are an evaluator. Return only a rating (digit 1–5), an explanation (1–2 sentences), and a rewritten summary (max 100 words). Do not generate steps, transcripts, or reasoning. Do not include any other text."},
    {"role": "user", "content": """Transcript:
Paul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.

Summary:
Andros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.

STRICT output format (must follow exactly):
Rating: <digit 1–5>
Explanation: <short explanation, one or two sentences>
Summary: <concise summary in max 100 words>"""}
]

# Build tokenized input properly (dictionary, not tensor)
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
inputs = {"input_ids": inputs.to("cuda" if torch.cuda.is_available() else "cpu")}

# Generate
output = model.generate(
    **inputs,
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    repetition_penalty=1.1,
    eos_token_id=tokenizer.eos_token_id,
)

# Decode
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)











# Build the chat in proper format
messages = [
    {"role": "system", "content": "You are an evaluator. Return only a rating (digit 1–5), an explanation (1–2 sentences), and a rewritten summary (max 100 words). Do not generate steps, transcripts, or reasoning. Do not include any other text."},
    {"role": "user", "content": """Transcript:
Paul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.

Summary:
Andros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.

STRICT output format (must follow exactly):
Rating: <digit 1–5>
Explanation: <short explanation, one or two sentences>
Summary: <concise summary in max 100 words>"""}
]

# Turn into proper input IDs with chat template
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

# Generate
output = model.generate(**inputs, max_new_tokens=512, temperature=0.7, top_p=0.9, do_sample=True, repetition_penalty=1.1)

# Decode
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)




prompt = "<s>[INST] <<SYS>> You are an evaluator. Return only a rating (digit 1–5), an explanation (1–2 sentences), and a rewritten summary (max 100 words). Do not generate steps, transcripts, or reasoning. Do not include any other text. <</SYS>> Transcript: Paul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution. Summary: Andros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half. STRICT output format (must follow exactly): Rating: <digit 1–5> Explanation: <short explanation, one or two sentences> Summary: <concise summary in max 100 words> [/INST]"



prompt = "Example:\nTranscript: Short text about a footballer improving in a match.\nSummary: Player improved after criticism.\nOutput:\nRating: 4\nExplanation: The summary captures the main idea but misses minor details.\nSummary: The player faced criticism but performed well later and was praised.\n\nNow your turn:\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nOutput:"



prompt = "Transcript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nOutput strictly in this format:\nRating: <1-5>\nExplanation: <1-2 sentences>\nSummary: <concise summary in max 100 words>"





prompt = "Example:\nRating: 4\nExplanation: The summary captures most main points but misses a detail about gradual improvement.\nSummary: Townsend clashed with Paul Ince over his England performance but impressed in Tottenham’s match against Burnley, where Merson praised his improvement.\n\nNow do the same for this case:\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nYour turn:"




prompt = "Fill the following template based on the transcript and summary.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nTemplate:\nRating: \nExplanation: \nSummary:"





prompt = "Based on the transcript and summary, replace the placeholders in this template ONLY:\nRating: <number between 1 and 5>\nExplanation: <1-2 sentences>\nSummary: <concise summary in max 100 words>\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nYour response must ONLY be the filled template. Nothing else."





prompt = "Fill in the following template based on the transcript and summary.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nTemplate:\nRating: \nExplanation: \nSummary:"




prompt = "Evaluate the following summary against the transcript and fill in the template.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nTemplate:\nRating: \nExplanation: \nSummary:"




prompt = "Evaluate the summary against the transcript and respond in exactly this format:\n\nRating: 4\nExplanation: The summary captures most of the key points but misses minor details.\nSummary: <your concise rewritten summary here>\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half."



prompt = "You are a strict evaluator. Respond ONLY in exactly three lines and nothing else. The format is:\nRating: <number between 1 and 5>\nExplanation: <1-2 sentences>\nSummary: <concise summary in max 100 words>\nIf you output anything else, even one extra word or step, your answer is invalid.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nFinal Answer (only 3 lines):"




prompt = "You are a strict evaluator. You must output EXACTLY three lines and nothing else. The format is:\nRating: <number between 1 and 5>\nExplanation: <1-2 sentences>\nSummary: <concise summary in max 100 words>\nDo NOT add anything before or after these three lines. Do NOT repeat the instructions. Do NOT explain your reasoning. If you fail to follow this format, your answer is invalid.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nFinal Answer:"



prompt = "You are a strict evaluator. Output MUST be exactly three lines in this exact format:\nRating: <number between 1 and 5>\nExplanation: <1–2 sentences>\nSummary: <concise summary in max 100 words>\nIf you output anything else, even one extra word, your answer is invalid.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half.\n\nYour response must begin now:"




prompt = "Instructions: You are a strict evaluator. Output MUST be exactly three lines in this exact format:\nRating: <number between 1 and 5>\nExplanation: <1–2 sentences>\nSummary: <concise summary in max 100 words>\nIf you output anything else, even one extra word, your answer is invalid.\n\nNow evaluate the following:\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half."





prompt = "You are a strict evaluator. Output MUST be exactly three lines in this exact format:\nRating: <number between 1 and 5>\nExplanation: <1–2 sentences>\nSummary: <concise summary in max 100 words>\nIf you output anything else, even one extra word, your answer is invalid.\n\nTranscript:\nPaul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution.\n\nSummary:\nAndros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half."




prompt = "You are a strict evaluator. Your task is to assess the completeness of the summary compared to the transcript. Completeness means the summary should capture all important information from the transcript. Your output MUST follow this exact format, and nothing else: Rating: <number between 1 and 5> Explanation: <1–2 sentences only> Summary: <concise summary in max 100 words> RULES: - Do NOT output reasoning steps such as 'Step 1', 'Step 2', etc. - Do NOT explain your process. - Do NOT output anything other than Rating, Explanation, and Summary. - If you output anything extra, your answer is invalid. Transcript: Paul Merson has asserted his view on Andros Townsend after his appearance for Tottenham Hotspur in a match against Burnley. Merson stated that Townsend initially struggled but gradually improved and displayed quality, especially in the second half. Townsend had earlier clashed with Paul Ince on Twitter after Ince criticized him for his performance for England against Italy. The disagreement escalated as Townsend hit back, defending his inclusion in the England squad. This incident attracted mixed reactions from fans and pundits. Despite the controversy, Townsend showed promise during the Tottenham match, with Merson acknowledging his effort and contribution. Summary: Andros Townsend, after criticism from Paul Ince regarding his England performance, clashed with him on Twitter. Despite the criticism, Townsend impressed in Tottenham’s match against Burnley, where Paul Merson praised his improvement and quality, especially in the second half."






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





