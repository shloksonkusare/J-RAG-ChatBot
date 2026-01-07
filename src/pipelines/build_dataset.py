import sys

from src.login import logging
from src.exception import CustomException
from src.ingestion.pdf_loader import PDFLoader
from src.processing.cleaner import TextCleaner
from src.processing.chunker import TextChunker
from src.exporters.jsonl_writer import JSONLWriter


def build_grammar_dataset():
    try:
        logging.info("===== Grammar Dataset Pipeline Started =====")

        loader = PDFLoader("data/grammar/grammar_guide.pdf")
        pages = loader.load()

        cleaner = TextCleaner()
        chunker = TextChunker(max_chars=800)

        records = []

        for page_idx, page in enumerate(pages):
            logging.info(f"Processing page {page_idx + 1}")

            cleaned = cleaner.clean(page)
            chunks = chunker.chunk(cleaned)

            for chunk in chunks:
                records.append({
                    "text": chunk,
                    "type": "grammar",
                    "jlpt_level": "UNKNOWN",
                    "topic": "grammar/general",
                    "source": "Tae Kim Grammar Guide | Grammar"
                })

        writer = JSONLWriter("data/grammar/grammar.jsonl")
        writer.write(records)

        logging.info("===== Grammar Dataset Pipeline Completed Successfully =====")

    except Exception as e:
        logging.error("Grammar Dataset Pipeline Failed")
        raise CustomException(e, sys)


if __name__ == "__main__":
    build_grammar_dataset()
