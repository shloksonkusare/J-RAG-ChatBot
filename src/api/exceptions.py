from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.login import logging
from src.exception import CustomException


async def custom_exception_handler(request: Request, exc: CustomException):
    """
    Handles CustomException raised inside RAG / pipelines
    """
    logging.error(f"CustomException: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong while processing your request."
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles FastAPI validation errors
    """
    logging.warning(f"Validation error: {exc}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all fallback for unexpected errors
    """
    logging.exception("Unhandled exception occurred")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Unexpected server error occurred."
        }
    )
