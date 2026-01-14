importance = xgb_model.get_score(importance_type="gain")

importance_df = (
    pd.DataFrame(importance.items(), columns=["feature", "gain"])
    .sort_values("gain", ascending=False)
)

print(importance_df.head(20))


from sklearn.inspection import permutation_importance
import pandas as pd

r = permutation_importance(
    clf,
    X_test,
    y_test,
    n_repeats=5,
    random_state=42,
    scoring="roc_auc"
)

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": r.importances_mean
}).sort_values("importance", ascending=False)

print(importance_df.head(20))






# Already created for TabPFN
# X_train, X_test, y_train, y_test

import xgboost as xgb

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="aucpr",
    scale_pos_weight=scale_pos_weight,
    tree_method="hist",
    device="cuda",
    random_state=42
)

model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    verbose=50
)









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

