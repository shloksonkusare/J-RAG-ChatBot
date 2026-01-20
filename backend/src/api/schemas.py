from pydantic import BaseModel
from typing import Optional, Literal, List
import uuid


class ChatRequest(BaseModel):
    query: str
    jlpt_level: Optional[str] = None
    content_type: Optional[str] = "grammar"
    session_id: Optional[str] = None


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
