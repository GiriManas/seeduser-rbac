from transformers.utils import hub
import torch

model_path = "Qwen/Qwen2_v1_7B-Instruct"

# Load tokenizer as usual
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Load model class dynamically from model repo (bypasses AutoModel logic)
model_class = hub.get_class_from_dynamic_module(
    "modeling_qwen2_v1.Qwen2ForCausalLM",  # file + class in the model repo
    pretrained_model_name_or_path=model_path,
    trust_remote_code=True,
)

model = model_class.from_pretrained(
    model_path,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16
)