import os
import time
import numpy as np
import torch
from tabpfn import TabPFNClassifier


def main():
    # --------------------------------------------------
    # Environment (offline + NAS)
    # --------------------------------------------------
    os.environ["HF_HOME"] = "/mnt/nas1/giri/huggingface"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["TABPFN_OFFLINE"] = "1"

    CKPT_PATH = (
        "/mnt/nas1/giri/huggingface/tabpfn_2_5/"
        "tabpfn-v2.5-classifier-v2.5_default.ckpt"
    )

    # --------------------------------------------------
    # GPU sanity check
    # --------------------------------------------------
    print("Torch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available in this pod")

    print("GPU:", torch.cuda.get_device_name(0))

    # --------------------------------------------------
    # Simulated transaction data
    # --------------------------------------------------
    np.random.seed(42)
    n = 1000

    amount = np.random.lognormal(mean=7.5, sigma=1.0, size=n)
    time_since_last_txn = np.random.exponential(scale=300, size=n)
    txn_count_24h = np.random.poisson(lam=3, size=n)
    balance_before = np.random.lognormal(mean=8.0, sigma=1.2, size=n)

    X = np.column_stack([
        amount,
        np.log1p(amount),
        time_since_last_txn,
        txn_count_24h,
        balance_before,
        balance_before - amount
    ])

    y = (
        (amount > np.percentile(amount, 95))
        & (time_since_last_txn < 60)
        & (txn_count_24h > 3)
    ).astype(int)

    noise_idx = np.random.choice(n, size=int(0.05 * n), replace=False)
    y[noise_idx] = 1 - y[noise_idx]

    # --------------------------------------------------
    # Model load (GPU)
    # --------------------------------------------------
    t0 = time.perf_counter()
    clf = TabPFNClassifier(
        device="cuda",           # 🔥 GPU enabled
        model_path=CKPT_PATH
    )
    t1 = time.perf_counter()
    print(f"⏱ Model load time (GPU): {t1 - t0:.3f}s")

    # --------------------------------------------------
    # Warm-up (VERY IMPORTANT for GPU timing)
    # --------------------------------------------------
    clf.fit(X[:50], y[:50])
    _ = clf.predict(X[:50])
    torch.cuda.synchronize()

    # --------------------------------------------------
    # Fit timing
    # --------------------------------------------------
    t2 = time.perf_counter()
    clf.fit(X, y)
    torch.cuda.synchronize()
    t3 = time.perf_counter()
    print(f"⏱ fit() time (GPU): {t3 - t2:.3f}s")

    # --------------------------------------------------
    # Predict timing
    # --------------------------------------------------
    t4 = time.perf_counter()
    preds = clf.predict(X)
    probs = clf.predict_proba(X)[:, 1]
    torch.cuda.synchronize()
    t5 = time.perf_counter()
    print(f"⏱ predict() time (GPU): {t5 - t4:.3f}s")

    # --------------------------------------------------
    # Evaluation
    # --------------------------------------------------
    from sklearn.metrics import roc_auc_score, average_precision_score

    auc = roc_auc_score(y, probs)
    pr_auc = average_precision_score(y, probs)

    print(f"AUC: {auc:.4f}")
    print(f"PR-AUC: {pr_auc:.4f}")

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------
    del clf
    torch.cuda.empty_cache()
    os._exit(0)


if __name__ == "__main__":
    main()