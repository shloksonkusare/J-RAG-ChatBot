import os
import sys
from typing import List

from dotenv import load_dotenv
from groq import Groq

from src.login import logging
from src.exception import CustomException


# Load environment variables from .env
load_dotenv()


class AnswerGenerator:
    """
    Answer generation using Groq-hosted LLMs
    """

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")

            self.client = Groq(api_key=api_key)
            self.model = model

            logging.info("Groq AnswerGenerator initialized successfully")

        except Exception as e:
            logging.error("Failed to initialize Groq AnswerGenerator")
            raise CustomException(e, sys)

    def generate_answer(self, query: str, contexts: List[str]) -> str:
        try:
            logging.info("Generating answer using Groq LLM")

            context_text = "\n".join(contexts[:5])

            prompt = (
                "You are a Japanese language tutor.\n\n"
                "Use the context below to answer the question clearly and simply.\n\n"
                f"Context:\n{context_text}\n\n"
                f"Question:\n{query}\n\n"
                "Answer:"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logging.error("Groq answer generation failed")
            raise CustomException(e, sys)
