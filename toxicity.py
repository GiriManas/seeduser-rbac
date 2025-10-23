"""
Toxicity Metric (Enhanced)
--------------------------
Evaluates and compares toxicity of a transcript and its generated summary.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F


def compute_toxicity_score(
    transcript,
    summary: str,
    model_name: str = "unitary/toxic-bert",
    device: str = None
):
    """
    Compute toxicity for transcript (str or list[str]) and summary.

    Args:
        transcript (str or list[str]): Original transcript text(s).
        summary (str): Generated summary text.
        model_name (str): Toxicity model (default: 'unitary/toxic-bert').
        device (str): 'cuda' or 'cpu'.

    Returns:
        dict: {
            "metric": "toxicity",
            "transcript_mean": float,
            "summary_mean": float,
            "delta": float,
            "transcript_scores": dict[str, float],
            "summary_scores": dict[str, float]
        }
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Handle transcript as str or list
    if isinstance(transcript, list):
        transcript_text = " ".join(transcript)
    else:
        transcript_text = transcript

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)

    def _get_scores(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)[0].cpu().numpy()

        labels = [
            "toxic", "severe_toxic", "obscene",
            "threat", "insult", "identity_hate"
        ]
        return {label: round(float(p), 4) for label, p in zip(labels, probs)}

    # Compute toxicity for both transcript and summary
    transcript_scores = _get_scores(transcript_text)
    summary_scores = _get_scores(summary)

    transcript_mean = round(sum(transcript_scores.values()) / len(transcript_scores), 4)
    summary_mean = round(sum(summary_scores.values()) / len(summary_scores), 4)

    # Δ (delta) = summary toxicity - transcript toxicity
    delta = round(summary_mean - transcript_mean, 4)

    return {
        "metric": "toxicity",
        "transcript_mean": transcript_mean,
        "summary_mean": summary_mean,
        "delta": delta,
        "transcript_scores": transcript_scores,
        "summary_scores": summary_scores
    }


# Example usage
if __name__ == "__main__":
    transcript = [
        "Customer was upset about charges and used harsh words.",
        "Agent tried to calm the customer down."
    ]
    summary = "Customer was angry with the agent about unexpected charges."
    result = compute_toxicity_score(transcript, summary)
    print(result)