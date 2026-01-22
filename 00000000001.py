start_time = time.time()

X_tensor = torch.tensor(
    X_test_history.values,
    device="cuda",
    dtype=torch.float32
)

preds = []
probs = []
batch = 8192

for i in range(0, len(X_tensor), batch):
    proba = clf.predict_proba(X_tensor[i:i+batch])
    probs.append(proba[:, 1])
    preds.append((proba[:, 1] > 0.5).astype(int))

y_pred = np.concatenate(preds)
y_prob = np.concatenate(probs)

print(f"Prediction time: {time.time() - start_time:.2f}s")