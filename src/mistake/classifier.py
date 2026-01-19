class MistakeClassifier:
    """
    Classifies the type of mistake
    """

    @staticmethod
    def classify(text: str) -> str:
        if "は" in text and "が" in text:
            return "particle_contrast"

        if "ですか" in text:
            return "question_form"

        if "を" in text:
            return "particle_usage"

        return "general_grammar"
