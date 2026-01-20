import os
import sys
from typing import List, Dict, Optional

from dotenv import load_dotenv
from groq import Groq

from src.login import logging
from src.exception import CustomException

# Load environment variables
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

    # -------------------------
    # Prompt Templates
    # -------------------------

    def _normal_prompt(
        self,
        query: str,
        context_text: str,
        memory_text: str
    ) -> str:
        return f"""
You are a Japanese language tutor.

You MUST answer using ONLY the information provided in the context.
If a section cannot be answered from the context, write:
"Not found in context."

Previous Conversation (for reference only):
{memory_text}

IMPORTANT:
- Use memory ONLY to understand follow-up questions
- DO NOT repeat previous answers
- DO NOT use memory as a knowledge source

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

    def _mistake_prompt(
        self,
        query: str,
        context_text: str,
        memory_text: str,
        mistake_type: str
    ) -> str:
        return f"""
You are a Japanese language tutor.

The user's sentence contains a GRAMMATICAL MISTAKE.
Mistake type: {mistake_type}

You MUST explain the mistake using ONLY the information provided in the context.
Do NOT invent grammar rules.

Previous Conversation (for reference only):
{memory_text}

IMPORTANT:
- Do NOT use memory as a knowledge source
- Do NOT soften the mistake — explain clearly and politely
- Do NOT invent rules or sources

Context:
{context_text}

User Sentence:
{query}

Your response MUST follow this exact structure:

Mistake Explanation:
- Why the sentence is incorrect

Correct Rule:
- The correct grammar rule

Corrected Examples:
- <correct example 1>
- <correct example 2>

Contrast:
- ❌ <incorrect usage>
- ✔ <correct usage>

DO NOT invent sources.
"""

    # -------------------------
    # Public API
    # -------------------------

    def generate_answer(
        self,
        query: str,
        contexts: List[str],
        metadatas: List[Dict],
        memory_text: str = "",
        mistake_type: Optional[str] = None
    ) -> str:
        """
        Generate a structured, source-attributed answer.
        """
        try:
            logging.info("Generating answer via Groq LLM")

            context_text = "\n".join(contexts[:5])

            # ---- Source attribution (deterministic) ----
            sources = set()
            for meta in metadatas:
                source = meta.get("source", "Unknown source")
                topic = meta.get("topic", "Unknown section")
                sources.add(f"- {source} (Section: {topic})")

            source_block = "\n".join(sorted(sources)) if sources else "- Unknown source"

            # ---- Prompt selection ----
            if mistake_type:
                prompt = self._mistake_prompt(
                    query=query,
                    context_text=context_text,
                    memory_text=memory_text,
                    mistake_type=mistake_type
                )
            else:
                prompt = self._normal_prompt(
                    query=query,
                    context_text=context_text,
                    memory_text=memory_text
                )

            # ---- LLM Call ----
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            answer_text = response.choices[0].message.content.strip()

            return (
                f"{answer_text}\n\n"
                "Source:\n"
                f"{source_block}"
            )

        except Exception as e:
            logging.error("Answer generation failed")
            raise CustomException(e, sys)
