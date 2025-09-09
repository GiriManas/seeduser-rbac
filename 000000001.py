# --------------------------
# Helper: robust parser (improved for Phi + Gemma)
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    """
    Parse generated_text to extract rating (int 1–5) and explanation (string).
    Works for both Gemma (clean) and Phi (messy, JSON-like, lowercase).
    """
    if not generated_text or not isinstance(generated_text, str):
        return None, None

    s = generated_text.strip()

    # Clean stray braces/quotes
    s = re.sub(r'^[\s\{\[\"]+|[\s\}\]\"]+$', '', s)
    s = s.replace("**", "").replace("*", "")

    # 1) Match "Rating: 4" or "rating - 4"
    m = re.search(r"[Rr]ating\s*[:=\-]?\s*([1-5])", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()

        # Try to cut explanation at "Explanation:" if it exists
        m2 = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", explanation, re.DOTALL)
        if m2:
            explanation = m2.group(1).strip()
        return rating, explanation

    # 2) Match "Explanation: ..." directly
    m = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", s, re.DOTALL)
    if m:
        explanation = m.group(1).strip()
        # Look for digit before it
        digit = re.search(r"\b([1-5])\b", s[:m.start()])
        rating = int(digit.group(1)) if digit else None
        return rating, explanation

    # 3) Standalone digit (avoid picking from scale definition)
    prefix = s[:200]
    for mm in re.finditer(r"\b([1-5])\b", prefix):
        idx_end = mm.end()
        after = s[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):  # skip scale definitions like "1 = very inaccurate"
            continue
        rating = int(mm.group(1))
        explanation = s[idx_end:].strip()
        return rating, explanation

    # 4) If nothing found
    return None, s.strip()
    
    
    
    
