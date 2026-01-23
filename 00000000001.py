batch = 8192
preds, probs = [], []

for i in range(0, len(X_test_history), batch):
    X_batch = X_test_history.iloc[i:i+batch]

    proba = clf.predict_proba(X_batch)
    probs.append(proba[:, 1])
    preds.append((proba[:, 1] > 0.5).astype(int))