from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.api.routes import router
from src.api.exceptions import (
    custom_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from src.exception import CustomException
from src.login import logging


# -----------------------------
# Rate Limiter Setup
# -----------------------------
limiter = Limiter(key_func=get_remote_address)


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="J-RAG-ChatBot API",
    description="Japanese Learning RAG Backend",
    version="1.0.0"
)

# Attach limiter to app state (IMPORTANT)
app.state.limiter = limiter


# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Routes
# -----------------------------
app.include_router(router)


# -----------------------------
# Exception Handlers
# -----------------------------

# Custom project exceptions
app.add_exception_handler(CustomException, custom_exception_handler)

# Request validation errors
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logging.warning(f"Rate limit exceeded for {request.client.host}")
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later."
        }
    )

# Fallback for unexpected errors
app.add_exception_handler(Exception, generic_exception_handler)
