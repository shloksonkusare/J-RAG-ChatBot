from pydantic import BaseModel
from typing import Optional, Literal, List


class ChatRequest(BaseModel):
    query: str
    jlpt_level: Optional[Literal["N5", "N4", "N3", "N2", "N1"]] = None
    content_type: Optional[Literal["grammar", "vocab"]] = "grammar"


class ChatResponse(BaseModel):
    answer: str


class QuizRequest(BaseModel):
    query: str
    jlpt_level: Optional[str] = None
    content_type: Optional[str] = "grammar"


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]
