import pandas as pd
import numpy as np
from typing import Dict, Any


def convert_tabular_to_fraud_transactions(
    df: pd.DataFrame,
    account_id_col: str,
    column_types: Dict[str, str],
    timestamp_col: str = None,
    sort_by_time: bool = True,
    N: int = 100,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Converts tabular transaction data into a fraud-focused dataset using
    window logic (fraud + prior rows) and 1:N non-fraud sampling.

    Returns:
        pd.DataFrame
    """

    # ------------------------------------------------------------------
    # 1. Copy input to avoid side effects
    # ------------------------------------------------------------------
    working_df = df.copy()

    # ------------------------------------------------------------------
    # 2. Type conversions
    # ------------------------------------------------------------------
    pandas_type_map = {
        "str": "string",
        "string": "string",
        "text": "string",
        "float": "float64",
        "double": "float64",
        "int": "Int64",
        "integer": "Int64",
    }

    for col, dtype in column_types.items():
        if col not in working_df.columns:
            continue

        dtype = dtype.lower()

        if dtype in ["int", "integer"]:
            working_df[col] = pd.to_numeric(
                working_df[col], errors="coerce"
            ).astype("Int64")

        elif dtype in ["float", "double"]:
            working_df[col] = pd.to_numeric(
                working_df[col], errors="coerce"
            ).astype("float64")

        elif dtype in ["string", "str", "text"]:
            working_df[col] = working_df[col].astype("string")

        elif dtype in ["date", "datetime", "timestamp"]:
            working_df[col] = pd.to_datetime(
                working_df[col], errors="coerce"
            )

    # ------------------------------------------------------------------
    # 3. Sort (optional but REQUIRED for correct window behavior)
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
    # 4. Fraud block logic (window foundation)
    # ------------------------------------------------------------------
    # Each fraud creates a new block per account
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
    # 5. Fraud + 4 prior rows
    # ------------------------------------------------------------------
    fraud_window_df = working_df[
        (working_df["frd_tag"] == 1) |
        (
            (working_df["fraud_block"] > 0) &
            (working_df["row_in_block"] <= 4)
        )
    ]

    # ------------------------------------------------------------------
    # 6. Eligible non-fraud rows
    # ------------------------------------------------------------------
    eligible_nonfraud = working_df[
        (working_df["frd_tag"] == 0) &
        (working_df["fraud_block"] > 0)
    ]

    # ------------------------------------------------------------------
    # 7. Fraud counts per account (for 1:N sampling)
    # ------------------------------------------------------------------
    fraud_counts = (
        working_df
        .groupby(account_id_col)["frd_tag"]
        .sum()
    )

    # ------------------------------------------------------------------
    # 8. Sample non-fraud rows (1 : N per account)
    # ------------------------------------------------------------------
    sampled_nonfraud = (
        eligible_nonfraud
        .groupby(account_id_col, group_keys=False)
        .apply(
            lambda x: x.sample(
                n=min(
                    len(x),
                    max(1, int(fraud_counts.loc[x.name] * N))
                ),
                random_state=random_state
            )
        )
    )

    # ------------------------------------------------------------------
    # 9. Final dataset
    # ------------------------------------------------------------------
    final_df = (
        pd.concat([fraud_window_df, sampled_nonfraud])
        .drop_duplicates()
        .sort_values(
            [account_id_col, timestamp_col]
            if sort_by_time else [account_id_col]
        )
        .reset_index(drop=True)
    )

    return final_df