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






# if no rating found yet, scan the whole output for the first 1–5 not part of a scale
m = re.search(r"\b([1-5])\b", s)
if m:
    rating = int(m.group(1))
    explanation = s[m.end():].strip()
    return rating, explanation