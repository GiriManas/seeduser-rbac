# --------------------------
# Phi-4 specific prompt template
# --------------------------
prompt_template = """You are an evaluator. 
Compare the given summary with the transcript and assign a groundedness rating.

Instructions (STRICT):
- Rating must be an integer between 1 and 5
- Output format MUST start with one of the following:
   1) A single digit (e.g. 4) on the first line
   2) Or: "Rating: 4" on the first line
- After the rating, provide a clear explanation in plain text.
- Do NOT include the transcript or the summary again in your response.
- Do NOT output any other sections, headers, or commentary.

Transcript:
{source}

Summary:
{summary}

Now produce only the rating and explanation in the required format.
"""






def parse_rating_and_explanation(generated_text: str):
    """
    Parse generated_text to extract rating (int 1-5) and explanation (string).
    Works even if Phi outputs rating buried deeper in text.
    """
    s = (generated_text or "").strip()

    # Case 1: Exact first-line digit
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # Case 2: Rating: 4
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # Case 3: "4/5"
    m = re.search(r"([1-5])\s*/\s*5", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    # Case 4: Scan first ~200 chars for a stray digit 1-5 not part of scale definition
    prefix = s[:200]
    for mm in re.finditer(r"([1-5])", prefix):
        idx_end = mm.end()
        after = s[idx_end: idx_end + 4]
        if re.match(r"\s*=", after):  # skip "1 = very inaccurate" etc
            continue
        rating = int(mm.group(1))
        explanation = s[idx_end:].strip()
        return rating, explanation

    # Case 5: Last fallback → no rating found
    return None, s.strip()