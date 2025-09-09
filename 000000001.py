# --------------------------
# Parser
# --------------------------
def parse_rating_and_explanation(text: str):
    if not text or text.strip() == "":
        return None, None
    s = text.strip()

    # case 1: "Rating: 4"
    m = re.search(r"Rating\s*[:\-]?\s*([1-5])", s, re.IGNORECASE)
    if m:
        return int(m.group(1)), s[m.end():].strip()

    # case 2: digit on first line
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        return int(m.group(1)), s[m.end():].strip()

    # case 3: "Explanation:" section
    m = re.search(r"Explanation\s*[:\-]?\s*(.*)", s, re.DOTALL | re.IGNORECASE)
    if m:
        return None, m.group(1).strip()

    return None, s

# --------------------------
# Extract results
# --------------------------
ratings, explanations = [], []
for raw in df["raw_evaluation"]:
    rating, explanation = parse_rating_and_explanation(raw)

    if rating is None and raw and raw.strip():
        # Fallback: ask model again ONLY if raw has some content
        rescue_prompt = f"Extract only the rating (a single digit 1–5) from the following text:\n\n{raw}"
        inputs = tokenizer(rescue_prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            rescue_out = model.generate(**inputs, max_new_tokens=16, do_sample=False)
        rescue_decoded = tokenizer.decode(rescue_out[0], skip_special_tokens=True).strip()

        # stricter match: rating must be isolated
        m = re.search(r"^(?:Rating\s*[:\-]?\s*)?([1-5])$", rescue_decoded, re.IGNORECASE | re.MULTILINE)
        if m:
            rating = int(m.group(1))

    explanations.append(clean_explanation(explanation))
    ratings.append(rating)

df["rating"] = ratings
df["explanation"] = explanations