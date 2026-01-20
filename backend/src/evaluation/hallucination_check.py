from typing import List


def hallucination_check(answer: str, contexts: List[str]) -> bool:
    """
    Returns True if answer is grounded in context, False otherwise.
    Simple heuristic-based check.
    """

    context_text = " ".join(contexts).lower()
    answer_text = answer.lower()

    # If answer contains "Not found in context", it's safe
    if "not found in context" in answer_text:
        return True

    # Check if key nouns from answer appear in context
    answer_tokens = set(answer_text.split())
    context_tokens = set(context_text.split())

    overlap_ratio = len(answer_tokens & context_tokens) / max(len(answer_tokens), 1)

    # Threshold can be tuned
    return overlap_ratio > 0.25
