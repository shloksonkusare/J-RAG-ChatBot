import sys
import json
from typing import List, Dict

from src.login import logging
from src.exception import CustomException


class QuizGenerator:
    """
    Generates Japanese learning quizzes using retrieved context
    """

    def __init__(self, answer_generator):
        self.client = answer_generator.client
        self.model = answer_generator.model

    def generate_quiz(self, contexts: List[str]) -> List[Dict]:
        try:
            if not contexts:
                return []

            logging.info("Generating quiz from retrieved context")

            context_text = "\n".join(contexts[:5])

            prompt = f"""
You are a Japanese language tutor.

Using ONLY the context below, generate 5 multiple-choice questions (MCQs).

Rules:
- Each question must have exactly 4 options
- Only ONE correct answer
- Provide a short explanation
- Output MUST be valid JSON
- Do NOT include markdown
- Do NOT include extra text

Context:
{context_text}

Output format:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "explanation": "..."
  }}
]
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            raw_output = response.choices[0].message.content.strip()

            # 🔒 SAFE parsing
            return json.loads(raw_output)

        except json.JSONDecodeError:
            logging.error("LLM returned invalid JSON for quiz")
            raise CustomException("Quiz generation failed due to invalid format", sys)

        except Exception as e:
            logging.error("Quiz generation failed")
            raise CustomException(e, sys)
