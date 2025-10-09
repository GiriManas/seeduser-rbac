@torch.no_grad()
def predict(self, passage, source):
    premise = " ".join(passage) if isinstance(passage, list) else passage

    # Generate facts from LLaMA
    result = self.llm_pipeline(self.VQ_generate_template.format(passage=source))
    facts = [tmp for tmp in result[0]['generated_text'].split('\n') if len(tmp) > 3]

    if len(facts) == 0:
        return np.mean([-0.5]), [-0.5], []

    res = []
    for tmp in facts:
        inputs = self.tokenizer.encode_plus(
            premise, tmp, padding=True, truncation=True, return_tensors='pt'
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        outputs = self.model(**inputs)
        logits = outputs.logits if hasattr(outputs, "logits") else outputs[0]
        probs = torch.softmax(logits, dim=-1)
        entail_prob = probs[:, 2].item()  # Entailment label probability
        res.append(entail_prob)

    return np.mean(res), res, facts









def create_default_llama_pipeline(config=None):
    global DEFAULT_llama_model_, DEFAULT_llama_tokenizer_, DEFAULT_llama_pipeline_, DEFAULT_llama_config_

    # Load the shared model if not already initialized
    if DEFAULT_llama_model_ is None:
        DEFAULT_llama_model_ = LlamaForCausalLM.from_pretrained(
            LLAMA2_CHAT_7B,
            torch_dtype=torch.float16,
            device_map="auto"  # Let HF manage placement automatically
        )

    # Load the shared tokenizer if not already initialized
    if DEFAULT_llama_tokenizer_ is None:
        DEFAULT_llama_tokenizer_ = LlamaTokenizer.from_pretrained(LLAMA2_CHAT_7B)

    # Create the shared pipeline only once
    if DEFAULT_llama_pipeline_ is None:
        if config is None:
            config = DEFAULT_llama_config_
        else:
            DEFAULT_llama_config_ = config

        DEFAULT_llama_pipeline_ = pipeline(
            "text-generation",
            model=DEFAULT_llama_model_,          # reuse existing model
            tokenizer=DEFAULT_llama_tokenizer_,  # reuse existing tokenizer
            device='cuda',                       # generic CUDA device (let PyTorch pick)
            return_full_text=False,
            do_sample=True,
            **config
        )

    return DEFAULT_llama_pipeline_