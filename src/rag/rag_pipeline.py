import sys
import re
from typing import List

from src.embeddings.embedder import Embedder
from src.vector_db.chroma_client import ChromaClient
from src.translation.translator import Translator
from src.llm.answer_generator import AnswerGenerator
from src.login import logging
from src.exception import CustomException


def is_japanese(text: str) -> bool:
    """
    Detect if text contains Japanese characters
    """
    return bool(re.search(r"[\u3040-\u30ff\u4e00-\u9faf]", text))


class RAGPipeline:
    def __init__(self):
        try:
            self.embedder = Embedder()
            self.db = ChromaClient()
            self.answer_generator = AnswerGenerator()

            self.ja_en_translator = Translator(direction="ja-en")
            self.en_ja_translator = Translator(direction="en-ja")

            logging.info("RAGPipeline initialized successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def run(self, query: str, top_k: int = 5) -> str:
        try:
            logging.info(f"Received query: {query}")

            original_language = "ja" if is_japanese(query) else "en"

            # Step 1: Translate query if needed
            if original_language == "ja":
                logging.info("Japanese query detected, translating to English")
                query_en = self.ja_en_translator.translate([query])[0]
            else:
                query_en = query

            # Step 2: Embed query
            query_embedding = self.embedder.embed_texts([query_en])[0]

            # Step 3: Retrieve contexts
            results = self.db.similarity_search(
                query_embedding,
                top_k=top_k,
                where={"type": "grammar"}
            )

            contexts: List[str] = results["documents"][0]

            # Step 4: Generate answer (English)
            answer_en = self.answer_generator.generate_answer(
                query=query_en,
                contexts=contexts
            )

            # # Step 5: Translate answer back if needed
            # if original_language == "ja":
            #     logging.info("Translating answer back to Japanese")
            #     answer_final = self.en_ja_translator.translate([answer_en])[0]
            # else:
            #     answer_final = answer_en

            # return answer_final
            return answer_en

        except Exception as e:
            logging.error("RAGPipeline failed")
            raise CustomException(e, sys)
