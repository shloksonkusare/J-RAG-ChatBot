import sys
import json
from pathlib import Path

from src.login import logging
from src.exception import CustomException
from src.embeddings.embedder import Embedder
from src.vector_db.chroma_client import ChromaClient


def load_jsonl(file_path: str):
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records


def build_embeddings():
    try:
        logging.info("===== Embedding Pipeline Started =====")

        data_files = [
            "data\\grammar\\grammar.jsonl",
            "data\\vocabulary\\jlpt_vocab.jsonl",
        ]

        texts = []
        metadatas = []
        ids = []

        for file_path in data_files:
            if not Path(file_path).exists():
                logging.warning(f"File not found, skipping: {file_path}")
                continue

            logging.info(f"Loading data from {file_path}")
            records = load_jsonl(file_path)

            for idx, record in enumerate(records):
                texts.append(record["text"])
                metadatas.append({
                    "type": record["type"],
                    "jlpt_level": record["jlpt_level"],
                    "topic": record["topic"],
                    "source": record["source"]
                })
                ids.append(f"{Path(file_path).stem}_{idx}")

        logging.info(f"Total documents to embed: {len(texts)}")

        embedder = Embedder()
        embeddings = embedder.embed_texts(texts)

        db = ChromaClient()
        db.add_documents(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        logging.info("===== Embedding Pipeline Completed Successfully =====")

    except Exception as e:
        logging.error("Embedding Pipeline Failed")
        raise CustomException(e, sys)


if __name__ == "__main__":
    build_embeddings()
