import sys
from src.login import logging
from src.exception import CustomException


class TextChunker:
    def __init__(self, max_chars: int = 800):
        self.max_chars = max_chars
        logging.info(f"TextChunker initialized with max_chars={self.max_chars}")

    def chunk(self, text: str) -> list[str]:
        try:
            logging.info("Starting text chunking")

            chunks = []
            current = ""

            for sentence in text.split(". "):
                if len(current) + len(sentence) < self.max_chars:
                    current += sentence + ". "
                else:
                    chunks.append(current.strip())
                    current = sentence + ". "

            if current:
                chunks.append(current.strip())

            logging.info(f"Text chunking completed. Total chunks: {len(chunks)}")
            return chunks

        except Exception as e:
            logging.error("Error occurred during text chunking")
            raise CustomException(e, sys)
