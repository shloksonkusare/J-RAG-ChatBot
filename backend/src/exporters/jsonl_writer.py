import json
import sys
from pathlib import Path

from src.login import logging
from src.exception import CustomException


class JSONLWriter:
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        logging.info(f"JSONLWriter initialized with output path: {self.output_path}")

    def write(self, records: list[dict]):
        try:
            logging.info("Starting JSONL write process")

            self.output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.output_path, "w", encoding="utf-8") as f:
                for idx, record in enumerate(records):
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

                    if idx % 100 == 0:
                        logging.info(f"Wrote {idx + 1} records")

            logging.info(f"JSONL writing completed. Total records: {len(records)}")

        except Exception as e:
            logging.error("Error occurred while writing JSONL file")
            raise CustomException(e, sys)
