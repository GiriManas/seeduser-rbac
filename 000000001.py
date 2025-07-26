from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch
from app.configuration import MODEL_HUB, PHI_3_MINI_4K_INSTRUCT, PHI_3_MINI_120K_INSTRUCT


def load_phi_model(MODEL_REF):
    print("====================LOADING {model} MODEL START ====================".format(model=MODEL_REF))
    model_dir = MODEL_HUB + MODEL_REF

    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        trust_remote_code=True,
        torch_dtype=torch.float16
    ).cuda()

    # ---------------- PATCH FOR DynamicCache ----------------
    if hasattr(model, "prepare_inputs_for_generation"):
        orig_prepare = model.prepare_inputs_for_generation

        def patched_prepare_inputs_for_generation(*args, **kwargs):
            if "past_key_values" in kwargs:
                pkv = kwargs["past_key_values"]
                # Add get_max_length dynamically
                if hasattr(pkv, "get_seq_length") and not hasattr(pkv, "get_max_length"):
                    pkv.get_max_length = pkv.get_seq_length
            return orig_prepare(*args, **kwargs)

        model.prepare_inputs_for_generation = patched_prepare_inputs_for_generation
    # --------------------------------------------------------

    gen_config = GenerationConfig.from_pretrained(model_dir)
    print("====================LOADING {model} MODEL COMPLETE ====================".format(model=MODEL_REF))
    return tokenizer, model, gen_config


# Load 120k model
tokenizer_phi_3_mini_120k_instruct, model_phi_3_mini_120k_instruct, gen_config_phi_3_mini_120k_instruct = \
    load_phi_model(PHI_3_MINI_120K_INSTRUCT)