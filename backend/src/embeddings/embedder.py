import sys
from typing import List

from sentence_transformers import SentenceTransformer

from src.login import logging
from src.exception import CustomException


class Embedder:
    """
    Responsible for converting text into embeddings
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        try:
            logging.info(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logging.info("Embedding model loaded successfully")

        except Exception as e:
            logging.error("Failed to load embedding model")
            raise CustomException(e, sys)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert list of texts into embeddings
        """
        try:
            logging.info(f"Generating embeddings for {len(texts)} texts")

            embeddings = self.model.encode(
                texts,
                show_progress_bar=True,
                convert_to_numpy=True
            )

            logging.info("Embeddings generated successfully")
            return embeddings.tolist()

        except Exception as e:
            logging.error("Failed while generating embeddings")
            raise CustomException(e, sys)
