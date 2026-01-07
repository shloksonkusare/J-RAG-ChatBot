from pathlib import Path
import pdfplumber
import sys

from src.login import logging
from src.exception import CustomException


class PDFLoader:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        logging.info(f"Initialized PDFLoader with path: {self.pdf_path}")

    def load(self) -> list[str]:
        try:
            if not self.pdf_path.exists():
                raise FileNotFoundError(f"{self.pdf_path} not found")

            pages = []
            logging.info(f"Opening PDF file: {self.pdf_path}")

            with pdfplumber.open(self.pdf_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        pages.append(text)
                        logging.info(f"Extracted text from page {idx + 1}")

            logging.info(f"Total pages extracted: {len(pages)}")
            return pages

        except Exception as e:
            logging.error("Error occurred while loading PDF")
            raise CustomException(e, sys)
