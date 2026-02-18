
#Step 1 — Filter Non-Frauds in Cluster 4

df_c4_nfraud = df_c4[df_c4['label'] == 0]

#Step 2 — Rank by Suspiciousness

We define suspicious non-frauds as:
	1.	High model probability (probs)
	2.	Close to fraud-dense region in embedding space
	3.	High-risk feature values (amount, length, etc.)
    
df_suspicious = df_c4_nfraud.sort_values('probs', ascending=False)
df_suspicious.head(20)

These are non-frauds with highest fraud probability inside a fraud-heavy cluster.










from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30,
    n_iter=1000
)

embeddings_2d = tsne.fit_transform(embeddings_sub)










from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42, perplexity=30)
emb_c4_2d = tsne.fit_transform(emb_c4)










import numpy as np

mask_c4 = (cluster_ids == 4)

emb_c4 = embeddings_sub[mask_c4]
labels_c4 = labels_sub[mask_c4]

print(emb_c4.shape)
print(labels_c4.shape)



from sklearn.cluster import KMeans

kmeans_c4 = KMeans(n_clusters=3, random_state=42)
subcluster_ids = kmeans_c4.fit_predict(emb_c4)




import pandas as pd

df_c4_new = pd.DataFrame({
    "subcluster": subcluster_ids,
    "label": labels_c4
})

df_c4_new.groupby("subcluster")["label"].agg(
    count="count",
    fraud_rate="mean"
).sort_values("fraud_rate", ascending=False)


















plt.scatter(df_c4[df_c4.label==1]['emb_2d_x'],
            df_c4[df_c4.label==1]['emb_2d_y'], alpha=0.3)

plt.scatter(df_c4[df_c4.label==0]['emb_2d_x'],
            df_c4[df_c4.label==0]['emb_2d_y'], alpha=0.3)

plt.legend(['Fraud','Non-Fraud'])
plt.show()








if logits.shape[-1] == 2:
    probs = torch.softmax(logits, dim=1)[:, 1]
else:
    probs = torch.sigmoid(logits).squeeze(-1)

all_probs.append(probs.detach().cpu().numpy())










def model_forward_with_logits(batch):

    input_ids = batch["input_ids"].to(device)
    lens = batch["lens"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):

            # Backbone
            outputs = clf_model.model(input_ids=input_ids)
            hidden_states = outputs["hidden_states"]   # 👈 IMPORTANT

            # Last valid token pooling
            idx = (lens - 1).clamp_min(0)
            pooled = hidden_states[
                torch.arange(hidden_states.size(0), device=hidden_states.device),
                idx
            ]

            # Fraud head
            pooled = clf_model.dropout(pooled)
            logits = clf_model.score(pooled)

    return hidden_states, logits







def model_forward_with_logits(batch):

    input_ids = batch["input_ids"].to(device)
    lens = batch["lens"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            
            # 1️⃣ Get backbone hidden states
            hidden_states = clf_model.model(input_ids=input_ids)
            # shape: [B, T, 2048]

            # 2️⃣ Last valid token pooling
            idx = (lens - 1).clamp_min(0)
            pooled = hidden_states[
                torch.arange(hidden_states.size(0), device=hidden_states.device),
                idx
            ]
            # shape: [B, 2048]

            # 3️⃣ Fraud head
            pooled = clf_model.dropout(pooled)
            logits = clf_model.score(pooled)
            # shape: [B, 1]

    return hidden_states, logits











def model_forward_with_logits(batch):

    input_ids = batch['input_ids'].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):

            model = clf_model.model

            x = model.token_embedding(input_ids)
            x = model.pos_embedding(x)

            for layer in model.layers:
                x = layer(x)

            hidden_states = model.norm(x)
            logits = model.lm_head(hidden_states)

    return hidden_states, logits








# Concatenate everything
embeddings = np.vstack(all_embs)          # [N, D]
labels = np.concatenate(all_labels)       # [N]
probs = np.concatenate(all_probs)         # [N]

print("Embeddings:", embeddings.shape)
print("Labels:", labels.shape)
print("Probs:", probs.shape)

# Save
np.save("/mnt/common/.../embeddings.npy", embeddings.astype(np.float32))
np.save("/mnt/common/.../labels.npy", labels.astype(np.int8))
np.save("/mnt/common/.../probs.npy", probs.astype(np.float32))

print("Saved successfully")












pooled = hidden[
    torch.arange(hidden.size(0), device=hidden.device),
    idx
]


if logits.shape[-1] == 2:
    probs = torch.softmax(logits, dim=1)[:, 1]
else:
    probs = torch.sigmoid(logits).squeeze(-1)
    
    
    
    all_probs.append(probs.detach().cpu().numpy())


print(hidden.shape)   # should be [256, T, 2048]
print(logits.shape)   # should be [256, 1] or [256, 2]
print(lens.shape)     # should be [256]
break


hidden, logits = model_forward_with_logits(batch)



def model_forward_with_logits(batch):

    input_ids = batch['input_ids'].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            outputs = clf_model.model(input_ids=input_ids)

    return outputs["hidden_states"], outputs["logits"]






def model_forward(batch):

    input_ids = batch["input_ids"].to(device)

    with torch.no_grad():
        with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            outputs = clf_model.model(input_ids=input_ids)

    return outputs





all_embs = []
all_labels = []
all_probs = []

clf_model.model.eval()

for batch in tqdm(eval_dataloader, desc="Processing Validation Data"):

    batch = {k: v.to(device) if isinstance(v, torch.Tensor) else v
             for k, v in batch.items()}

    outputs = model_forward(batch)

    hidden_states = outputs.hidden_states[-1]   # last transformer layer
    logits = outputs.logits                     # classifier logits

    lens = batch["lens"]
    labels = batch["frd_labels"]

    # -------- Last token pooling --------
    idx = (lens - 1).clamp_min(0)
    pooled = hidden_states[torch.arange(hidden_states.size(0)), idx]

    # -------- Convert logits → probability --------
    if logits.shape[-1] == 2:
        probs = torch.softmax(logits, dim=1)[:, 1]  # probability of fraud
    else:
        probs = torch.sigmoid(logits).squeeze()

    all_embs.append(pooled.detach().cpu().numpy())
    all_labels.append(labels.detach().cpu().numpy())
    all_probs.append(probs.detach().cpu().numpy())
    
    
    
    
embeddings = np.vstack(all_embs)
labels = np.concatenate(all_labels)
probs = np.concatenate(all_probs)

print("Embeddings shape:", embeddings.shape)
print("Labels shape:", labels.shape)
print("Probs shape:", probs.shape)









base_path = "/nas/pyfrm_dev_3/mrm/pfm/debit/trans_0624_1024_byacct/"

files = [f"{base_path}part_{i}" for i in range(1, 6)]

df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)







cluster_fraud_rate = df.groupby("Cluster")["label"].mean()


fraud_rate_per_point = [cluster_fraud_rate[c] for c in cluster_ids]


plt.figure(figsize=(8,6))

plt.scatter(
    embeddings_2d[:, 0],
    embeddings_2d[:, 1],
    c=fraud_rate_per_point,
    cmap="Reds",
    s=5,
    alpha=0.7
)

plt.colorbar(label="Cluster Fraud Rate")
plt.title("Clusters Colored by Fraud Density")
plt.show()








import matplotlib.pyplot as plt

# Create masks
fraud_mask = labels_sub == 1
nonfraud_mask = labels_sub == 0

# Fix axis limits for fair comparison
x_min, x_max = embeddings_2d[:,0].min(), embeddings_2d[:,0].max()
y_min, y_max = embeddings_2d[:,1].min(), embeddings_2d[:,1].max()

plt.figure(figsize=(14,6))

# --- Non-Fraud ---
plt.subplot(1, 2, 1)
plt.scatter(
    embeddings_2d[nonfraud_mask, 0],
    embeddings_2d[nonfraud_mask, 1],
    s=5,
    alpha=0.6
)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.title("Non-Fraud")

# --- Fraud ---
plt.subplot(1, 2, 2)
plt.scatter(
    embeddings_2d[fraud_mask, 0],
    embeddings_2d[fraud_mask, 1],
    s=5,
    alpha=0.6
)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.title("Fraud")

plt.tight_layout()
plt.show()






import pandas as pd

df = pd.DataFrame({
    "cluster": cluster_ids,
    "label": labels_sub
})

cluster_stats = df.groupby("cluster").agg(
    count=("label", "count"),
    fraud_rate=("label", "mean")
).sort_values("fraud_rate", ascending=False)

cluster_stats









import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))

plt.scatter(
    embeddings_2d[labels_sub == 0, 0],
    embeddings_2d[labels_sub == 0, 1],
    alpha=0.2,
    label="Non-Fraud"
)

plt.scatter(
    embeddings_2d[labels_sub == 1, 0],
    embeddings_2d[labels_sub == 1, 1],
    alpha=0.8,
    label="Fraud"
)

plt.legend()
plt.title("Fraud vs Non-Fraud on t-SNE Space")
plt.show()






import numpy as np

np.random.seed(42)

MAX_POINTS = 20000

fraud_idx = np.where(labels == 1)[0]
nonfraud_idx = np.where(labels == 0)[0]

# Decide how many fraud to keep (cap at MAX_POINTS // 2)
max_fraud = MAX_POINTS // 2
n_fraud = min(len(fraud_idx), max_fraud)
n_nonfraud = MAX_POINTS - n_fraud

fraud_keep = np.random.choice(
    fraud_idx,
    size=n_fraud,
    replace=False
)

nonfraud_keep = np.random.choice(
    nonfraud_idx,
    size=n_nonfraud,
    replace=False
)

selected_idx = np.concatenate([fraud_keep, nonfraud_keep])
np.random.shuffle(selected_idx)

embeddings_sub = embeddings[selected_idx]
labels_sub = labels[selected_idx]

print("Subsampled embeddings:", embeddings_sub.shape)
print("Fraud count:", labels_sub.sum())
print("Fraud ratio:", labels_sub.mean())












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