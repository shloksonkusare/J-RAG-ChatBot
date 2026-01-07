import sys
from pathlib import Path
import pandas as pd

from src.login import logging
from src.exception import CustomException


class CSVLoader:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        logging.info(f"Initialized CSVLoader with path: {self.csv_path}")

    def load(self) -> list[dict]:
        """
        Loads CSV file and returns list of rows as dictionaries
        """
        try:
            if not self.csv_path.exists():
                raise FileNotFoundError(f"{self.csv_path} not found")

            logging.info(f"Reading CSV file: {self.csv_path}")

            df = pd.read_csv(self.csv_path)

            logging.info(
                f"CSV loaded successfully | Rows: {df.shape[0]} | Columns: {df.shape[1]}"
            )

            records = df.to_dict(orient="records")

            logging.info(f"Converted CSV to list of dictionaries")

            return records

        except Exception as e:
            logging.error("Error occurred while loading CSV file")
            raise CustomException(e, sys)
