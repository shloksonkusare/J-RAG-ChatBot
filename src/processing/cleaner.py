import re
import sys

from src.login import logging
from src.exception import CustomException


class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        try:
            logging.info("Starting text cleaning")

            text = re.sub(r'\n+', '\n', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()

            logging.info("Text cleaning completed")
            return text

        except Exception as e:
            logging.error("Error occurred during text cleaning")
            raise CustomException(e, sys)
