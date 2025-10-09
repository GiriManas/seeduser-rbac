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