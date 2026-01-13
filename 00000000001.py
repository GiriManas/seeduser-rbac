selected_row_indices = set()

group = group.reset_index()  # keep original index

fraud_indices = group.index[group['frd_tag'] == 1].tolist()

for idx in fraud_indices:
    selected_row_indices.add(group.loc[idx, 'index'])  # fraud row

    count = 0
    j = idx - 1
    while j >= 0 and count < 4:
        if group.loc[j, 'frd_tag'] == 1:
            break
        selected_row_indices.add(group.loc[j, 'index'])
        count += 1
        j -= 1
        
        
import numpy as np

N = 100  # ratio

nonfraud_idxs = group.index[group['frd_tag'] == 0].tolist()

sample_size = max(1, len(fraud_indices) * N)
sample_size = min(sample_size, len(nonfraud_idxs))

sampled_nonfraud = np.random.choice(
    nonfraud_idxs,
    size=sample_size,
    replace=False
)

for idx in sampled_nonfraud:
    selected_row_indices.add(group.loc[idx, 'index'])

    count = 0
    j = idx - 1
    while j >= 0 and count < 4:
        if group.loc[j, 'frd_tag'] == 1:
            break
        selected_row_indices.add(group.loc[j, 'index'])
        count += 1
        j -= 1
        
return working_df.loc[sorted(selected_row_indices)].reset_index(drop=True)