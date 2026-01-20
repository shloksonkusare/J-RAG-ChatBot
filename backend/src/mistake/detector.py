import re


class MistakeDetector:
    """
    Detects whether a user input is likely a grammatical mistake
    """

    @staticmethod
    def is_likely_mistake(text: str) -> bool:
        # Common Japanese mistake patterns
        patterns = [
            r"は.*ですか",      # incorrect question pattern
            r"を.*です",        # misuse of を
            r"が.*ください",    # incorrect particle usage
        ]

        for pattern in patterns:
            if re.search(pattern, text):
                return True

        # English mistake signals
        english_signals = [
            "is this correct",
            "am i right",
            "is this wrong",
            "correct sentence",
        ]

        text_lower = text.lower()
        return any(signal in text_lower for signal in english_signals)
