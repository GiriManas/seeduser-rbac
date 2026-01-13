import pandas as pd
from typing import Dict


def convert_tabular_to_fraud_transactions(
    df: pd.DataFrame,
    account_id_col: str,
    column_types: Dict[str, str],
    timestamp_col: str = None,
    sort_by_time: bool = True,
    N: int = 100,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Extract fraud transactions with up to 4 prior transactions and
    sample 1:N non-fraud transactions per account.

    Returns a DataFrame with the SAME structure as input df.
    """

    # ------------------------------------------------------------------
    # 1. Work on a copy
    # ------------------------------------------------------------------
    working_df = df.copy()

    # ------------------------------------------------------------------
    # 2. Type conversions (as per specification)
    # ------------------------------------------------------------------
    for col, dtype in column_types.items():
        if col not in working_df.columns:
            continue

        dtype = dtype.lower()

        if dtype in ("int", "integer"):
            working_df[col] = pd.to_numeric(
                working_df[col], errors="coerce"
            ).astype("Int64")

        elif dtype in ("float", "double"):
            working_df[col] = pd.to_numeric(
                working_df[col], errors="coerce"
            )

        elif dtype in ("str", "string", "text"):
            working_df[col] = working_df[col].astype("string")

        elif dtype in ("date", "datetime", "timestamp"):
            working_df[col] = pd.to_datetime(
                working_df[col], errors="coerce"
            )

    # ------------------------------------------------------------------
    # 3. Sort by account + time (REQUIRED for window logic)
    # ------------------------------------------------------------------
    if sort_by_time:
        if timestamp_col is None:
            raise ValueError("timestamp_col must be provided when sort_by_time=True")

        working_df = (
            working_df
            .sort_values([account_id_col, timestamp_col])
            .reset_index(drop=True)
        )

    # ------------------------------------------------------------------
    # 4. Window logic (fraud blocks)
    # ------------------------------------------------------------------
    if sort_by_time:
        # Fraud block counter per account
        working_df["fraud_block"] = (
            working_df
            .groupby(account_id_col)["frd_tag"]
            .cumsum()
        )

        # Row number inside each fraud block
        working_df["row_in_block"] = (
            working_df
            .groupby([account_id_col, "fraud_block"])
            .cumcount()
        )

        # ------------------------------------------------------------------
        # 5. Fraud rows + up to 4 prior rows
        # ------------------------------------------------------------------
        fraud_window_df = working_df[
            (working_df["frd_tag"] == 1) |
            (
                (working_df["fraud_block"] > 0) &
                (working_df["row_in_block"] <= 4)
            )
        ]

        # ------------------------------------------------------------------
        # 6. 1:N non-fraud sampling (based on fraud count per account)
        # ------------------------------------------------------------------
        fraud_counts = (
            working_df
            .groupby(account_id_col)["frd_tag"]
            .sum()
        )

        eligible_nonfraud = working_df[
            (working_df["frd_tag"] == 0) &
            (working_df["fraud_block"] > 0)
        ]

        sampled_nonfraud = (
            eligible_nonfraud
            .groupby(account_id_col, group_keys=False)
            .apply(
                lambda x: x.sample(
                    n=min(len(x), max(1, fraud_counts.loc[x.name] * N)),
                    random_state=random_state
                )
            )
        )

        # ------------------------------------------------------------------
        # 7. Final result
        # ------------------------------------------------------------------
        final_df = (
            pd.concat([fraud_window_df, sampled_nonfraud])
            .drop_duplicates()
            .sort_values([account_id_col, timestamp_col])
            .reset_index(drop=True)
        )

    else:
        # No ordering → no window logic possible
        final_df = working_df.copy()

    return final_df