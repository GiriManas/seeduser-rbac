prompt_template = """You are evaluating the quality of a summary against the transcript.

Provide ONLY in this exact format (strict, no extra words, no transcript, no summary):
Rating: <digit 1-5>
Explanation: <your explanation of why the rating was given, without repeating transcript or summary text>

Transcript:
{source}

Summary:
{summary}
"""




def clean_explanation(text: str, max_len: int = 800):
    if not text:
        return ""

    # remove repeated prompt fragments
    text = re.sub(r"Transcript:.*?Summary:", "", text, flags=re.DOTALL | re.IGNORECASE)

    # aggressively remove "customer:" / "agent:" lines if leaked
    text = re.sub(r"(customer:|agent:).*", "", text, flags=re.IGNORECASE)

    # remove scale definitions
    text = re.sub(r"\b1\s*=\s*[^,.\n]*[,.\n]?\s*5\s*=\s*[^,.\n]*", "", text, flags=re.IGNORECASE)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # truncate
    if len(text) > max_len:
        text = text[:max_len].rstrip() + " ..."

    return text