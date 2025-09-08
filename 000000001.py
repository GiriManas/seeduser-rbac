IMPORTANT: Output must start with either:
- A single digit (1–5) on the first line
- Or "Rating: <digit>" on the first line
Do not include transcript or summary text again.





# if no rating found yet, scan the whole output for the first 1–5 not part of a scale
m = re.search(r"\b([1-5])\b", s)
if m:
    rating = int(m.group(1))
    explanation = s[m.end():].strip()
    return rating, explanation