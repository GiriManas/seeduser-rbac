import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score
from tqdm import tqdm

# -----------------------------
# Load saved TabPFN model
# -----------------------------
clf = joblib.load("model_tabpfn.joblib")

# -----------------------------
# SAMPLE ROWS (CRITICAL FOR SPEED)
# -----------------------------
N_SAMPLES = 20000   # 15k–30k is ideal
RANDOM_STATE = 42

X_sample = X_train_base.sample(
    n=min(N_SAMPLES, len(X_train_base)),
    random_state=RANDOM_STATE
)
y_sample = y_train_base.loc[X_sample.index]

print(f"Using {len(X_sample)} rows for permutation importance")

# -----------------------------
# Base prediction (DO ONCE)
# -----------------------------
print("Running baseline prediction...")
y_prob_base = clf.predict_proba(X_sample)[:, 1]
base_auc = roc_auc_score(y_sample, y_prob_base)

print(f"Baseline ROC-AUC: {base_auc:.6f}")

# -----------------------------
# Features to test
# (you said ~90 columns — this is fine)
# -----------------------------
FEATURES_TO_TEST = X_sample.columns.tolist()

# -----------------------------
# Permutation Importance
# -----------------------------
results = []

rng = np.random.default_rng(RANDOM_STATE)

for col in tqdm(FEATURES_TO_TEST, desc="TabPFN Permutation Importance"):
    X_perm = X_sample.copy()

    # Shuffle ONLY this column
    X_perm[col] = rng.permutation(X_perm[col].values)

    # Predict
    y_prob_perm = clf.predict_proba(X_perm)[:, 1]
    perm_auc = roc_auc_score(y_sample, y_prob_perm)

    results.append({
        "feature": col,
        "perm_auc": perm_auc,
        "importance": base_auc - perm_auc
    })

# -----------------------------
# Results dataframe
# -----------------------------
perm_imp_df = (
    pd.DataFrame(results)
      .sort_values("importance", ascending=False)
      .reset_index(drop=True)
)

print("\nTop 20 TabPFN Permutation Importances")
display(perm_imp_df.head(20))
