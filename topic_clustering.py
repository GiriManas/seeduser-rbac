import torch
from sentence_transformers import SentenceTransformer

if isinstance(sentence_embedding, str):
    model_loaded = False
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            try:
                device = f"cuda:{i}"
                print(f"Trying SentenceTransformer on {device}")
                self.embedding_model = SentenceTransformer(sentence_embedding, device=device)
                _ = self.embedding_model.encode("test")  # trigger allocation
                print(f"Model successfully loaded on {device}")
                model_loaded = True
                break
            except RuntimeError as e:
                if "CUDA out of memory" in str(e):
                    print(f"{device} out of memory. Trying next GPU...")
                else:
                    raise e
    if not model_loaded:
        print("Falling back to CPU.")
        self.embedding_model = SentenceTransformer(sentence_embedding, device="cpu")
else:
    self.embedding_model = sentence_embedding