import sys

from src.login import logging
from src.exception import CustomException
from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.csv_loader import CSVLoader
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
            logging.info(f"Processing grammar page {page_idx + 1}")

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


def build_vocab_dataset():
    try:
        logging.info("===== Vocabulary Dataset Pipeline Started =====")

        loader = CSVLoader("data\\vocabulary\\jlpt_vocab.csv")
        rows = loader.load()

        records = []

        for idx, row in enumerate(rows):
            try:
                word = str(row.get("Original", "")).strip()
                reading = str(row.get("Furigana", "")).strip()
                meaning = str(row.get("English", "")).strip()
                jlpt_level = str(row.get("JLPT Level", "UNKNOWN")).strip()

                if not word or not meaning:
                    logging.warning(f"Skipping row {idx} due to missing word/meaning")
                    continue

                text_parts = [word]
                if reading:
                    text_parts.append(f"({reading})")
                text_parts.append(f"— {meaning}")

                records.append({
                    "text": " ".join(text_parts),
                    "type": "vocab",
                    "jlpt_level": jlpt_level if jlpt_level else "UNKNOWN",
                    "topic": "vocabulary/general",
                    "source": "JLPT Vocabulary Dataset | Kaggle"
                })

                if idx % 500 == 0:
                    logging.info(f"Processed {idx} vocabulary records")

            except Exception as row_error:
                logging.warning(
                    f"Skipping vocab row {idx} due to error: {row_error}"
                )

        logging.info(f"Total vocabulary records created: {len(records)}")

        writer = JSONLWriter("data\\vocabulary\\jlpt_vocab.jsonl")
        writer.write(records)

        logging.info("===== Vocabulary Dataset Pipeline Completed Successfully =====")

    except Exception as e:
        logging.error("Vocabulary Dataset Pipeline Failed")
        raise CustomException(e, sys)


if __name__ == "__main__":
    build_grammar_dataset()
    build_vocab_dataset()
