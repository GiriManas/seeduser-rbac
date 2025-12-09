import pandas as pd
from pandas.tseries.offsets import MonthEnd

def filter_by_month_range(df, start_ym, end_ym=None, col='transaction_dtm'):
    # If only one month is provided → filter only that month
    if end_ym is None:
        start = pd.Timestamp(start_ym + '-01')
        end   = start + MonthEnd(1)  # End of given month
    else:
        start = pd.Timestamp(start_ym + '-01')
        end   = pd.Timestamp(end_ym + '-01') + MonthEnd(1)

    return df[(df[col] >= start) & (df[col] <= end)]