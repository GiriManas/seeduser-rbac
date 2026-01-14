import numpy as np
import pandas as pd

def prepare_xy(df, target_col="frd_tag"):
    df = df.copy()

    # Separate target
    y = df[target_col].astype(int).to_numpy()

    # Drop target from features
    X_df = df.drop(columns=[target_col])

    # Keep only numeric columns (important)
    X_df = X_df.select_dtypes(include=[np.number])

    # Handle missing values
    X_df = X_df.fillna(0)

    # Convert to numpy
    X = X_df.to_numpy(dtype=np.float32)

    print(f"Features used: {X.shape[1]}")
    print(f"Total rows: {X.shape[0]}")

    return X, y, X_df.columns.tolist()
    


from sklearn.model_selection import train_test_split

X, y, feature_names = prepare_xy(df)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y   # 🔥 critical for fraud
)

print("Train fraud rate:", y_train.mean())
print("Test fraud rate :", y_test.mean())




from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report
)

roc_auc = roc_auc_score(y_test, y_prob)
pr_auc = average_precision_score(y_test, y_prob)

print(f"ROC-AUC : {roc_auc:.4f}")
print(f"PR-AUC  : {pr_auc:.4f}")

print("\nClassification Report (0.5 threshold):")
print(classification_report(y_test, y_pred, digits=4))

del clf
torch.cuda.empty_cache()
os._exit(0)

