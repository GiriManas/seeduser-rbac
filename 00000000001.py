month_adv_filter = None
start_ym = None
end_ym = None

# Multi-month: 2024-11:2025-12 OR 112024:022025
if ":" in month:
    start_token, end_token = month.split(":")
    start_ym = normalize_month(start_token)
    end_ym   = normalize_month(end_token)
    month_adv_filter = f"{start_ym}:{end_ym}"

# Single month: 102024 / 2024-10 / 10-2024
else:
    start_ym = normalize_month(month)
    end_ym = None
    month_adv_filter = start_ym

# Retain month_idx ONLY if other parts of script still need it
month_idx = int(start_ym[-2:])