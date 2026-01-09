import sys
from typing import List, Dict

import chromadb
from chromadb.config import Settings

from src.login import logging
from src.exception import CustomException


class ChromaClient:
    """
    Handles vector storage and similarity search using ChromaDB
    """

    def __init__(
        self,
        persist_directory: str = "vector_store/chroma",
        collection_name: str = "japanese_rag"
    ):
        try:
            logging.info("Initializing ChromaDB Persistent Client")

            self.client = chromadb.PersistentClient(
                path=persist_directory
            )

            self.collection = self.client.get_or_create_collection(
                name=collection_name
            )

            logging.info(
                f"ChromaDB persistent collection ready: {collection_name}"
            )

        except Exception as e:
            logging.error("Failed to initialize ChromaDB Persistent Client")
            raise CustomException(e, sys)


    def add_documents(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict],
        batch_size: int = 500
    ):
        """
        Store embeddings in batches (ChromaDB auto-persists)
        """
        try:
            total = len(documents)
            logging.info(f"Adding {total} documents to ChromaDB in batches")

            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)

                logging.info(f"Adding batch {start} to {end}")

                self.collection.add(
                    ids=ids[start:end],
                    embeddings=embeddings[start:end],
                    documents=documents[start:end],
                    metadatas=metadatas[start:end]
                )

            logging.info("All documents added successfully (auto-persisted)")

        except Exception as e:
            logging.error("Failed to add documents to ChromaDB")
            raise CustomException(e, sys)



    def similarity_search(self, query_embedding, top_k=5, where=None):
        try:
            logging.info("Performing similarity search")

            query_args = {
                "query_embeddings": [query_embedding],
                "n_results": top_k
            }

            if where:
                query_args["where"] = where
                logging.info(f"Applying metadata filter: {where}")

            results = self.collection.query(**query_args)

            return results

        except Exception as e:
            logging.error("Similarity search failed")
            raise CustomException(e, sys)

