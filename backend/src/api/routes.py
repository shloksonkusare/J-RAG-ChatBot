from fastapi import APIRouter

from src.api.schemas import ChatRequest, ChatResponse
from src.rag.rag_pipeline import RAGPipeline
from src.api.schemas import QuizRequest, QuizResponse
from src.llm.quiz_generator import QuizGenerator
from src.memory.conversation_memory import ConversationMemory
import uuid



router = APIRouter()
rag = RAGPipeline()

SESSION_MEMORY = {}



@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = ConversationMemory(max_turns=5)

    memory = SESSION_MEMORY[session_id]

    answer = rag.run(
        query=request.query,
        jlpt_level=request.jlpt_level,
        content_type=request.content_type,
        conversation_memory=memory.get_memory()
    )

    memory.add_turn(request.query, answer)

    return {
        "answer": answer,
        "session_id": session_id
    }



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

