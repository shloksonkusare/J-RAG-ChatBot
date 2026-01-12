from fastapi import APIRouter

from src.api.schemas import ChatRequest, ChatResponse
from src.rag.rag_pipeline import RAGPipeline
from src.api.schemas import QuizRequest, QuizResponse
from src.llm.quiz_generator import QuizGenerator


router = APIRouter()
rag = RAGPipeline()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    General RAG-based chat endpoint with metadata filtering
    """
    answer = rag.run(
        query=request.query,
        jlpt_level=request.jlpt_level,
        content_type=request.content_type
    )
    return {"answer": answer}


@router.post("/explain", response_model=ChatResponse)
def explain(request: ChatRequest):
    """
    Grammar-focused explanation endpoint
    """
    answer = rag.run(
        query=request.query,
        jlpt_level=request.jlpt_level,
        content_type="grammar"
    )
    return {"answer": answer}


@router.post("/quiz", response_model=QuizResponse)
def quiz(request: QuizRequest):
    """
    Quiz generation endpoint
    """
    # Embed query
    embedding = rag.embedder.embed_texts([request.query])[0]

    # Build filter
    where_filter = {"type": request.content_type}
    if request.jlpt_level:
        where_filter["jlpt_level"] = request.jlpt_level

    results = rag.db.similarity_search(
        embedding,
        where=where_filter
    )

    contexts = results.get("documents", [[]])[0]

    if not contexts:
        return {"questions": []}

    quiz_generator = QuizGenerator(rag.answer_generator)
    questions = quiz_generator.generate_quiz(contexts)

    return {"questions": questions}

