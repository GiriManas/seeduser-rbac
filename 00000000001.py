# up to here: dtype conversion, timestamp parsing, sorting

# line 123
# account_groups = working_df.groupby(account_id_col)
# ⛔ do NOT use this anymore

# ✅ WINDOW-BASED LOGIC STARTS HERE
working_df = working_df.sort_values(
    [account_id_col, timestamp_col]
).reset_index(drop=True)

working_df['fraud_block'] = (
    working_df
    .groupby(account_id_col)['frd_tag']
    .cumsum()
)

working_df['row_in_block'] = (
    working_df
    .groupby([account_id_col, 'fraud_block'])
    .cumcount()
)

# Fraud + 4 prior rows
fraud_window_df = working_df[
    (working_df['frd_tag'] == 1) |
    (
        (working_df['fraud_block'] > 0) &
        (working_df['row_in_block'] <= 4)
    )
]

# 1:N non-fraud sampling
N = 100

eligible_nonfraud = working_df[
    (working_df['frd_tag'] == 0) &
    (working_df['fraud_block'] > 0)
]

fraud_counts = (
    working_df
    .groupby(account_id_col)['frd_tag']
    .sum()
)

sampled_nonfraud = (
    eligible_nonfraud
    .groupby(account_id_col, group_keys=False)
    .apply(
        lambda x: x.sample(
            n=min(len(x), max(1, fraud_counts.loc[x.name] * N)),
            random_state=42
        )
    )
)

final_df = (
    pd.concat([fraud_window_df, sampled_nonfraud])
    .drop_duplicates()
    .sort_values([account_id_col, timestamp_col])
    .reset_index(drop=True)
)

return final_df