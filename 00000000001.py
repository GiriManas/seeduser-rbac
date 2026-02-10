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