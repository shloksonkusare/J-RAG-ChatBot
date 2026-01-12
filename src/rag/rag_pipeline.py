import sys
import re
from typing import List, Optional

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

    def run(
        self,
        query: str,
        top_k: int = 5,
        jlpt_level: Optional[str] = None,
        content_type: str = "grammar"
    ) -> str:
        try:
            logging.info(
                f"Received query: {query} | "
                f"JLPT: {jlpt_level} | Type: {content_type}"
            )

            # ---- Day 14: Query guardrail ----
            if len(query.strip()) < 3:
                return "Please ask a more specific Japanese language question."

            original_language = "ja" if is_japanese(query) else "en"

            # Step 1: Translate query if needed
            if original_language == "ja":
                logging.info("Japanese query detected, translating to English")
                query_en = self.ja_en_translator.translate([query])[0]
            else:
                query_en = query

            # Step 2: Embed query
            query_embedding = self.embedder.embed_texts([query_en])[0]

            # ---- Day 15.2: Build dynamic metadata filter ----
            where_filter = {"type": content_type}

            if jlpt_level:
                where_filter["jlpt_level"] = jlpt_level

            logging.info(f"Chroma filter applied: {where_filter}")

            # Step 3: Retrieve contexts
            results = self.db.similarity_search(
                query_embedding,
                top_k=top_k,
                where=where_filter
            )

            contexts: List[str] = results.get("documents", [[]])[0]
            metadatas: List[dict] = results.get("metadatas", [[]])[0]

            # ---- Day 14: Empty retrieval safeguard ----
            if not contexts:
                return (
                    "Grammar Explanation:\n"
                    "Not found in context.\n\n"
                    "Rule:\n"
                    "Not found in context.\n\n"
                    "Usage:\n"
                    "Not found in context.\n\n"
                    "Examples:\n"
                    "- Not found in context.\n\n"
                    "Common Mistakes:\n"
                    "- Not found in context.\n\n"
                    "Source:\n"
                    "- No relevant source found"
                )

            # Step 4: Generate structured answer WITH source attribution
            answer = self.answer_generator.generate_answer(
                query=query_en,
                contexts=contexts,
                metadatas=metadatas
            )

            return answer

        except Exception as e:
            logging.error("RAGPipeline failed")
            raise CustomException(e, sys)
