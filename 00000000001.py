
# Fix object columns for XGBoost
obj_cols = X_train_base.select_dtypes(include=["object"]).columns

for c in obj_cols:
    X_train_base[c] = X_train_base[c].astype("category")
    X_test_base[c]  = X_test_base[c].astype("category")

xgb_model = XGBClassifier(
    tree_method="hist",
    enable_categorical=True,
    eval_metric="auc"
)

xgb_model.fit(
    X_train_base,
    y_train_base,
    eval_set=[(X_test_base, y_test_base)],
    verbose=True
)





import os

# ---- MUST COME FIRST ----
os.environ["HF_HOME"] = "/mnt/nas1/giri/huggingface"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["TABPFN_OFFLINE"] = "1"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# ---- THEN imports ----
import numpy as np
from tabpfn import TabPFNClassifier







batch = 8192
preds, probs = [], []

for i in range(0, len(X_test_history), batch):
    X_batch = X_test_history.iloc[i:i+batch]

    proba = clf.predict_proba(X_batch)
    probs.append(proba[:, 1])
    preds.append((proba[:, 1] > 0.5).astype(int))