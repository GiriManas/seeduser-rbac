import numpy as np
import pandas as pd

def prepare_xy(df, target_col="frd_tag"):
    df = df.copy()

    # Separate target
    y = df[target_col].astype(int).to_numpy()

    # Drop target from features
    X_df = df.drop(columns=[target_col])

    # Keep only numeric columns (important)
    X_df = X_df.select_dtypes(include=[np.number])

    # Handle missing values
    X_df = X_df.fillna(0)

    # Convert to numpy
    X = X_df.to_numpy(dtype=np.float32)

    print(f"Features used: {X.shape[1]}")
    print(f"Total rows: {X.shape[0]}")

    return X, y, X_df.columns.tolist()