def weighted_FPR_at_percentile(df, percentile, weight_column):
    df = df.copy()
    df = df.sort_values("prob", ascending=False)

    target = df["target"].values        # 1 = bad, 0 = good
    weight = df[weight_column].values

    # Identify goods
    is_good = (target == 0)

    # Total weighted goods (denominator)
    total_good_weight = np.sum(weight[is_good])
    if total_good_weight == 0:
        return np.nan

    # Cutoff by cumulative weight
    cumsum_weight = np.cumsum(weight)
    cutoff_weight = percentile * np.sum(weight)
    cutoff_idx = np.searchsorted(cumsum_weight, cutoff_weight)

    # False positives = goods selected in top bucket
    false_positive_weight = np.sum(weight[:cutoff_idx][is_good[:cutoff_idx]])

    # FPR
    return false_positive_weight / total_good_weight