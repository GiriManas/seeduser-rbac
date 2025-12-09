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
    
    

# Automatically filters from 2025-10-01 → 2025-10-31 23:59:59
df_oct2025 = filter_by_month_range(df, '2025-10')

# Works seamlessly over year boundaries. Includes all timestamps in those months
df_nov24_to_dec25 = filter_by_month_range(df, '2024-11', '2025-12')