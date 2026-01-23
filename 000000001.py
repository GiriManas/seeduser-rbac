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
# Base prediction (DO ONCE)
# -----------------------------
print("Running baseline prediction...")
y_prob_base = clf.predict_proba(X_test_history)[:, 1]
base_auc = roc_auc_score(y_test_history, y_prob_base)

print(f"Baseline ROC-AUC: {base_auc:.6f}")

# -----------------------------
# Choose features to test
# (IMPORTANT for speed)
# -----------------------------
FEATURES_TO_TEST = X_test_history.columns.tolist()
# or:
# FEATURES_TO_TEST = top_features_from_xgb[:50]

# -----------------------------
# Permutation Importance
# -----------------------------
results = []

for col in tqdm(FEATURES_TO_TEST, desc="Permutation Importance"):
    X_perm = X_test_history.copy()

    # Shuffle only THIS column
    X_perm[col] = np.random.permutation(X_perm[col].values)

    # Predict
    y_prob_perm = clf.predict_proba(X_perm)[:, 1]

    perm_auc = roc_auc_score(y_test_history, y_prob_perm)

    importance = base_auc - perm_auc

    results.append({
        "feature": col,
        "perm_auc": perm_auc,
        "importance": importance
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