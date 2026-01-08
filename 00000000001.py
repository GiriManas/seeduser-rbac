import os
import numpy as np
from tabpfn import TabPFNClassifier


def main():
    # --------------------------------------------------
    # Correct HF cache path (mounted NAS)
    # --------------------------------------------------
    os.environ["HF_HOME"] = "/mnt/nas1/huggingface"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    print("HF_HOME =", os.environ["HF_HOME"])

    # --------------------------------------------------
    # Dummy tabular data
    # --------------------------------------------------
    X = np.random.rand(50, 8)
    y = np.random.randint(0, 2, 50)

    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # --------------------------------------------------
    # Initialize TabPFN
    # IMPORTANT: no model_path here
    # --------------------------------------------------
    clf = TabPFNClassifier(
        device="cpu"   # change to "cuda" if allowed
    )

    print("TabPFNClassifier initialized")

    clf.fit(X, y)

    print("✅ TabPFN ran successfully")


if __name__ == "__main__":
    main()