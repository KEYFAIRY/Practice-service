from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    PosturalErrorNotFoundException,
    PracticeNotFoundException,
    ReportNotFoundException,
    PracticeServiceException,
    UserNotFoundException,
    DatabaseConnectionException,
    ValidationException
)
from app.presentation.schemas.common_schema import StandardResponse
import logging

logger = logging.getLogger(__name__)

def build_response(exc: PracticeServiceException) -> dict:
    logger.error(str(exc))

    return StandardResponse(
        code=str(exc.code),
        message=exc.message,
        data=exc.details or None
    ).dict()


async def practice_service_exception_handler(request: Request, exc: PracticeServiceException):
    logger.error(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def practice_not_found_exception_handler(request: Request, exc: PracticeNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def report_not_found_exception_handler(request: Request, exc: ReportNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def postural_error_not_found_exception_handler(request: Request, exc: PosturalErrorNotFoundException):
    logger.warning(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def database_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    logger.error(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

async def validation_exception_handler(request: Request, exc: ValidationException):
    logger.warning(str(exc))
    return JSONResponse(status_code=exc.code, content=build_response(exc))

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
