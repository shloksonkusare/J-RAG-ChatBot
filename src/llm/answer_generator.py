import os
import sys
from typing import List, Dict

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

    def generate_answer(
        self,
        query: str,
        contexts: List[str],
        metadatas: List[Dict]
    ) -> str:
        """
        Generate a structured, source-attributed answer.
        """
        try:
            logging.info("Generating structured answer with source attribution")

            context_text = "\n".join(contexts[:5])

            # Build deterministic source attribution
            sources = set()
            for meta in metadatas:
                source = meta.get("source", "Unknown source")
                topic = meta.get("topic", "Unknown section")
                sources.add(f"- {source} (Section: {topic})")

            source_block = "\n".join(sorted(sources)) if sources else "- Unknown source"

            prompt = f"""
                You are a Japanese language tutor.

                You MUST answer using ONLY the information provided in the context.
                If a section cannot be answered from the context, write:
                "Not found in context."

                Context:
                {context_text}

                Question:
                {query}

                Your response MUST follow this exact structure:

                Grammar Explanation:
                <explanation>

                Rule:
                <rule>

                Usage:
                <usage>

                Examples:
                - <example 1>
                - <example 2>

                Common Mistakes:
                - <mistake 1>
                - <mistake 2>

                DO NOT invent sources.
                """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            answer_text = response.choices[0].message.content.strip()

            final_answer = (
                f"{answer_text}\n\n"
                "Source:\n"
                f"{source_block}"
            )

            return final_answer

        except Exception as e:
            logging.error("Answer generation with sources failed")
            raise CustomException(e, sys)
