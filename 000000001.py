# llama_rating_pipeline_v1.py

import re
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# --------------------------
# Configurable column names
# --------------------------
COL_INTERACTION_ID = "cr_interactionid"
COL_TRANSCRIPT = "transcript"
COL_SUMMARY = "summary"
COL_RAW = "raw_evaluation"
COL_RATING = "rating"
COL_EXPLANATION = "explanation"

# --------------------------
# Load Llama model
# --------------------------
model_id = "meta-llama/Llama-3.2-3B-Instruct"   # change if needed
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
llama_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

# --------------------------
# Prompt template
# --------------------------
prompt_template = """You are an evaluator.
Read the transcript and its summary.
Give a groundedness rating from 1–5 (1 = very inaccurate, 5 = very accurate).
Do NOT repeat transcript or summary.

Now output ONLY in this exact format:
Rating: <digit between 1 and 5>
Explanation: <short explanation>

Transcript:
{source}

Summary:
{summary}
"""

# --------------------------
# Parser function
# --------------------------
def parse_rating_and_explanation(generated_text: str):
    if not generated_text or not isinstance(generated_text, str):
        return None, None

    s = generated_text.strip()
    s = re.sub(r'^[\s\{\[\"]+|[\s\}\]\"]+$', '', s)

    # Case 1: Match "Rating: 4"
    m = re.search(r"[Rr]ating\s*[:=\-]?\s*([1-5])", s)
    if m:
        rating = int(m.group(1))
        m2 = re.search(r"[Ee]xplanation\s*[:=\-]?\s*(.*)", s, re.DOTALL)
        explanation = m2.group(1).strip() if m2 else s[m.end():].strip()
        return rating, explanation

    # Case 2: Standalone digit at start
    m = re.match(r"^\s*([1-5])\s*(?:\n|$)", s)
    if m:
        rating = int(m.group(1))
        explanation = s[m.end():].strip()
        return rating, explanation

    return None, s.strip()

# --------------------------
# Fallback extraction prompt
# --------------------------
def fallback_extract_rating(raw_text: str):
    prompt = f"""The following text was generated but may not be structured well:

{raw_text}

Extract only the rating (1–5) and explanation.
Output strictly in this format:
Rating: <digit>
Explanation: <short explanation>"""

    out = llama_pipe(prompt, max_new_tokens=128, do_sample=False)
    parsed, expl = parse_rating_and_explanation(out[0]["generated_text"])
    return parsed, expl

# --------------------------
# Main evaluation function
# --------------------------
def evaluate_records(df: pd.DataFrame):
    ratings, explanations, raws = [], [], []

    for idx, row in df.iterrows():
        prompt = prompt_template.format(
            source=row[COL_TRANSCRIPT],
            summary=row[COL_SUMMARY]
        )
        out = llama_pipe(prompt, max_new_tokens=256, do_sample=False)
        raw_eval = out[0]["generated_text"]

        # Try parsing
        rating, explanation = parse_rating_and_explanation(raw_eval)

        # Fallback if missing rating
        if rating is None:
            rating, explanation = fallback_extract_rating(raw_eval)

        raws.append(raw_eval)
        ratings.append(rating)
        explanations.append(explanation)

        print(f"Row {idx} → rating={rating}, explanation preview={str(explanation)[:50]}")

    df[COL_RAW] = raws
    df[COL_RATING] = ratings
    df[COL_EXPLANATION] = explanations
    return df

# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # Example dummy dataframe
    data = {
        COL_INTERACTION_ID: [1, 2],
        COL_TRANSCRIPT: ["Agent: Hello, how can I help?", "Agent: Your card is blocked."],
        COL_SUMMARY: ["Greeting", "Card issue"],
    }
    df = pd.DataFrame(data)

    df_out = evaluate_records(df)
    print(df_out.head())
    df_out.to_csv("llama_ratings_output.csv", index=False)