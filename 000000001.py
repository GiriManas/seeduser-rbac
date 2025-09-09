def parse_rating_and_explanation(generated_text: str):
    """
    Parse model output to extract rating (1-5) and explanation.
    Stricter version: checks first line first, then falls back.
    """
    if not generated_text:
        return None, ""

    s = generated_text.strip()
    lines = s.splitlines()

    # --- 1) Strict first-line checks ---
    if lines:
        first_line = lines[0].strip()

        # Case: "Rating: 4"
        m = re.match(r"^Rating\s*[:\-]?\s*([1-5])$", first_line, re.IGNORECASE)
        if m:
            rating = int(m.group(1))
            explanation = " ".join(lines[1:]).strip()
            return rating, explanation

        # Case: just "4"
        m = re.match(r"^([1-5])$", first_line)
        if m:
            rating = int(m.group(1))
            explanation = " ".join(lines[1:]).strip()
            return rating, explanation

    # --- 2) Search anywhere for "Rating: 4" ---
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # --- 3) Search anywhere for "4/5" ---
    m = re.search(r"([1-5])\s*/\s*5", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # --- 4) Last fallback: first digit 1–5 in first 200 chars ---
    prefix = s[:200]
    for mm in re.finditer(r"([1-5])", prefix):
        idx_end = mm.end()
        after = s[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):  # skip scale definitions like "1 = very..."
            continue
        rating = int(mm.group(1))
        explanation = s[idx_end:].strip()
        return rating, explanation

    # --- 5) No rating found ---
    return None, s