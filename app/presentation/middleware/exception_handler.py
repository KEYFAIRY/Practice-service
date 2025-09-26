from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    PracticeNotFoundException,
    PracticeServiceException,
    UserNotFoundException,
    DatabaseConnectionException,
    ValidationException
)
from app.presentation.schemas.common_schema import StandardResponse
import logging

logger = logging.getLogger(__name__)

async def practice_service_exception_handler(request: Request, exc: PracticeServiceException):
    logger.error(f"PracticeServiceException: {exc.message} - Code: {exc.code}")
    response = StandardResponse.error(message=exc.message, code=exc.code)
    return JSONResponse(status_code=int(exc.code), content=response.dict())

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logger.warning(f"User not found: {exc.message}")
    response = StandardResponse.not_found(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())

async def practice_not_found_exception_handler(request: Request, exc: PracticeNotFoundException):
    logger.warning(f"Practice not found: {exc.message}")
    response = StandardResponse.not_found(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())

async def database_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    logger.error(f"Database connection error: {exc.message}")
    response = StandardResponse.internal_error(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())

async def validation_exception_handler(request: Request, exc: ValidationException):
    logger.warning(f"Validation error: {exc.message}")
    response = StandardResponse.validation_error(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Request validation error: {exc.errors()}")
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    formatted_message = "Validation errors: " + "; ".join(error_messages)
    response = StandardResponse.validation_error(formatted_message)
    return JSONResponse(status_code=422, content=response.dict())

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    response = StandardResponse.internal_error("An unexpected error occurred")
    return JSONResponse(status_code=500, content=response.dict())