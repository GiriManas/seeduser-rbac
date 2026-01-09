import os
import numpy as np
from tabpfn import TabPFNClassifier


def main():
    # ------------------------------------------------------------------
    # Environment setup (OpenShift + NAS)
    # ------------------------------------------------------------------
    os.environ["HF_HOME"] = "/mnt/nas1/giri/huggingface"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["TABPFN_OFFLINE"] = "1"   # extra safety

    # ------------------------------------------------------------------
    # Explicit checkpoint file (IMPORTANT: file, not directory)
    # ------------------------------------------------------------------
    CKPT_PATH = (
        "/mnt/nas1/giri/huggingface/tabpfn_2_5/"
        "tabpfn-v2.5-classifier-v2.5_default.ckpt"
    )

    print("HF_HOME:", os.environ["HF_HOME"])
    print("Using checkpoint:", CKPT_PATH)

    # ------------------------------------------------------------------
    # Dummy tabular data
    # ------------------------------------------------------------------
    np.random.seed(42)
    X = np.random.rand(50, 8)
    y = np.random.randint(0, 2, 50)

    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # ------------------------------------------------------------------
    # Initialize TabPFN
    # ------------------------------------------------------------------
    clf = TabPFNClassifier(
        device="cpu",          # change to "cuda" only if GPU is enabled
        model_path=CKPT_PATH   # 👈 MUST be a .ckpt file
    )

    print("TabPFNClassifier initialized")

    # ------------------------------------------------------------------
    # Fit (inference-style)
    # ------------------------------------------------------------------
    clf.fit(X, y)

    # ------------------------------------------------------------------
    # Predict
    # ------------------------------------------------------------------
    preds = clf.predict(X)
    probs = clf.predict_proba(X)

    print("Predictions (first 10):", preds[:10])
    print("Probabilities (first 5):", probs[:5])

    print("\n✅ TabPFN ran successfully using local NAS weights")


if __name__ == "__main__":
    main()