def normalize_month(token: str) -> str:
    token = token.strip()

    # Case 1: 'YYYY-MM' or 'MM-YYYY'
    if "-" in token:
        parts = token.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid month format: {token}")
        a, b = parts[0], parts[1]

        if len(a) == 4 and len(b) in (1, 2):   # '2024-10'
            year, month = a, b
        elif len(b) == 4 and len(a) in (1, 2): # '10-2024'
            year, month = b, a
        else:
            raise ValueError(f"Invalid month format: {token}")

    else:
        if len(token) != 6 or not token.isdigit():
            raise ValueError(f"Invalid month format: {token}")
        month, year = token[:2], token[2:]

    month = month.zfill(2)
    return f"{year}-{month}"