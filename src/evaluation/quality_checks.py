from typing import List, Dict


def retrieval_type_check(metadatas: List[Dict], expected_type: str) -> bool:
    """
    Ensures all retrieved chunks match expected content type.
    """
    for meta in metadatas:
        if meta.get("type") != expected_type:
            return False
    return True


def response_structure_check(answer: str) -> bool:
    """
    Ensures Day-11 structure is respected.
    """
    required_sections = [
        "Grammar Explanation:",
        "Rule:",
        "Usage:",
        "Examples:",
        "Common Mistakes:",
        "Source:"
    ]

    return all(section in answer for section in required_sections)
