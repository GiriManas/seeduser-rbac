import numpy as np

np.random.seed(42)

MAX_POINTS = 20000  # safe size for t-SNE

fraud_idx = np.where(labels == 1)[0]
nonfraud_idx = np.where(labels == 0)[0]

# keep all fraud
fraud_keep = fraud_idx

remaining = MAX_POINTS - len(fraud_keep)

nonfraud_keep = np.random.choice(
    nonfraud_idx,
    size=remaining,
    replace=False
)

selected_idx = np.concatenate([fraud_keep, nonfraud_keep])

embeddings_sub = embeddings[selected_idx]
labels_sub = labels[selected_idx]

print("Subsampled embeddings:", embeddings_sub.shape)
print("Fraud count:", labels_sub.sum())




from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate=200,
    random_state=42
)


embeddings_2d = tsne.fit_transform(embeddings_sub)

print("t-SNE output shape:", embeddings_2d.shape)


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=6, random_state=42)
cluster_ids = kmeans.fit_predict(embeddings_2d)


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=cluster_ids,
    alpha=0.6
)
plt.title("K-Means Clusters on t-SNE Output")
plt.show()


# Fraud Concentration Per cluster


import pandas as pd

df = pd.DataFrame({
    "cluster": cluster_ids,
    "label": labels_sub
})

stats = df.groupby("cluster").agg(
    count=("label", "count"),
    fraud_rate=("label", "mean")
).sort_values("fraud_rate", ascending=False)

print(stats)



import os

out_dir = "/nas/pyfrm_dev_3/mrm/pfm/experiments/fraud_ft/clustering/tsne_runs/last_token_run_001"
os.makedirs(out_dir, exist_ok=True)



import numpy as np

np.save(f"{out_dir}/selected_idx.npy", selected_idx)
np.save(f"{out_dir}/embeddings_sub.npy", embeddings_sub)
np.save(f"{out_dir}/labels_sub.npy", labels_sub)

print("Saved sampled embeddings and labels")



embeddings_2d = tsne.fit_transform(embeddings_sub)


np.save(f"{out_dir}/embeddings_2d_tsne.npy", embeddings_2d)

print("Saved t-SNE output:", embeddings_2d.shape)


np.save(f"{out_dir}/cluster_ids.npy", cluster_ids)



# Verify Everything loads

emb2d = np.load(f"{out_dir}/embeddings_2d_tsne.npy")
labs = np.load(f"{out_dir}/labels_sub.npy")

print(emb2d.shape, labs.shape)

embeddings_2d = np.load(".../embeddings_2d_tsne.npy")
labels_sub = np.load(".../labels_sub.npy")
cluster_ids = np.load(".../cluster_ids.npy")
















import numpy as np

embeddings = np.load(f"{base_path}/embeddings.npy")
labels = np.load(f"{base_path}/labels.npy")

print("Embeddings:", embeddings.shape)
print("Labels:", labels.shape)






import numpy as np

np.random.seed(42)

# Parameters
N_NON_FRAUD = 900
N_FRAUD = 100
D = 2048

# Non-fraud: large diffuse cluster
non_fraud_embeddings = np.random.normal(
    loc=0.0,
    scale=1.0,
    size=(N_NON_FRAUD, D)
)

# Fraud: tighter cluster, slightly shifted
fraud_embeddings = np.random.normal(
    loc=1.5,
    scale=0.6,
    size=(N_FRAUD, D)
)

# Combine
embeddings = np.vstack([non_fraud_embeddings, fraud_embeddings])
labels = np.array([0] * N_NON_FRAUD + [1] * N_FRAUD)

print("Embeddings shape:", embeddings.shape)
print("Labels shape:", labels.shape)




from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,
    learning_rate=200,
    random_state=42
)

embeddings_2d = tsne.fit_transform(embeddings)





import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

plt.scatter(
    embeddings_2d[labels == 0, 0],
    embeddings_2d[labels == 0, 1],
    alpha=0.3,
    label="Non-Fraud"
)

plt.scatter(
    embeddings_2d[labels == 1, 0],
    embeddings_2d[labels == 1, 1],
    alpha=0.8,
    label="Fraud"
)

plt.legend()
plt.title("t-SNE on Synthetic Embeddings")
plt.xlabel("t-SNE dim 1")
plt.ylabel("t-SNE dim 2")
plt.show()



from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, random_state=42)
cluster_ids = kmeans.fit_predict(embeddings)

plt.figure(figsize=(8, 6))
plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=cluster_ids,
    alpha=0.6
)
plt.title("K-Means clusters (synthetic data)")
plt.show()