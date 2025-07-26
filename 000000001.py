from torch.nn.utils.rnn import pad_sequence
import torch

def get_model_reponse(model_version: PhiVersionEnum = Query(..., description="Choose a model version"),
                      model_request: ModelPhiRequest = None):

    prompt = model_request.prompt
    tokenizer = tokenizer_phi_3_mini_120k_instruct  # Use 4K or 120K accordingly
    model = model_phi_3_mini_120k_instruct          # Use 4K or 120K accordingly

    # Tokenize with padding
    encodings = tokenizer(
        [prompt],
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]

    # Make sure pad_token_id is set
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # Move to device
    input_ids = input_ids.to(model.device)
    attention_mask = attention_mask.to(model.device)

    # Generate
    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"message": response}