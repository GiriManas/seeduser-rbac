import os
import numpy as np

from tabpfn import TabPFNClassifier


def main():
    # ------------------------------------------------------------------
    # Environment configuration (important for OpenShift / offline use)
    # ------------------------------------------------------------------
    os.environ["HF_HOME"] = "/nas/pyfrm_dev_3/huggingface"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    print("Environment variables set")
    print("HF_HOME =", os.environ["HF_HOME"])

    # ------------------------------------------------------------------
    # Create dummy tabular data (binary classification)
    # ------------------------------------------------------------------
    np.random.seed(42)

    X = np.random.rand(50, 8)   # 50 rows, 8 features
    y = np.random.randint(0, 2, 50)

    print("Dummy data created")
    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # ------------------------------------------------------------------
    # Initialize TabPFN
    # ------------------------------------------------------------------
    clf = TabPFNClassifier(
        device="cpu",  # change to "cuda" if GPU is allowed
        model_path="/nas/pyfrm_dev_3/huggingface/tabpfn_2_5"
    )

    print("TabPFNClassifier initialized")

    # ------------------------------------------------------------------
    # Fit (inference-style, no training)
    # ------------------------------------------------------------------
    clf.fit(X, y)
    print("TabPFN fit completed")

    # ------------------------------------------------------------------
    # Predict
    # ------------------------------------------------------------------
    y_pred = clf.predict(X)
    y_proba = clf.predict_proba(X)

    print("Predictions completed")
    print("Sample predictions:", y_pred[:10])
    print("Sample probabilities:", y_proba[:5])

    print("\n✅ TabPFN test run SUCCESSFUL")


if __name__ == "__main__":
    main()