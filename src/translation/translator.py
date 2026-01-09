import sys
from typing import List

from transformers import MarianMTModel, MarianTokenizer

from src.login import logging
from src.exception import CustomException


class Translator:
    """
    Free Japanese <-> English translation using MarianMT
    """

    def __init__(self, direction: str = "ja-en"):
        """
        direction:
            - "ja-en" : Japanese -> English
            - "en-ja" : English -> Japanese
        """
        try:
            if direction == "ja-en":
                model_name = "Helsinki-NLP/opus-mt-ja-en"
            elif direction == "en-ja":
                model_name = "staka/fugumt-en-ja"
            else:
                raise ValueError("direction must be 'ja-en' or 'en-ja'")

            logging.info(f"Loading translation model: {model_name}")

            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)

            logging.info("Translation model loaded successfully")

        except Exception as e:
            logging.error("Failed to initialize Translator")
            raise CustomException(e, sys)

    def translate(self, texts: List[str]) -> List[str]:
        """
        Translate a list of texts
        """
        try:
            logging.info(f"Translating {len(texts)} texts")

            tokens = self.tokenizer(
                texts,
                return_tensors="pt",
                padding=True,
                truncation=True
            )

            translated = self.model.generate(**tokens)

            outputs = [
                self.tokenizer.decode(t, skip_special_tokens=True)
                for t in translated
            ]

            logging.info("Translation completed successfully")
            return outputs

        except Exception as e:
            logging.error("Translation failed")
            raise CustomException(e, sys)
