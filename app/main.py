import logging
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exceptions import (
    DatabaseConnectionException,
    PracticeNotFoundException,
    PracticeServiceException,
    UserNotFoundException,
    ValidationException,
)
from app.infrastructure.database import mongo_connection, mysql_connection
from app.presentation.middleware.exception_handler import (
    database_connection_exception_handler,
    practice_not_found_exception_handler,
    practice_service_exception_handler,
    user_not_found_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler,
    general_exception_handler,
)
from app.presentation.api.v1.practice import router as get_practices


# Configure logging
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.APP_ENV}")

    # ---------- DB Connections ----------
    try:
        # MySQL
        mysql_connection.mysql_connection.init_engine()
        logger.info("MySQL connection established")

        # MongoDB
        mongo_connection.mongo_connection.connect()
        logger.info("MongoDB connection established")
        
    except DatabaseConnectionException as e:
        logger.exception("Error initializing database connections: " + str(e))
        raise

    yield

    # ---------- Shutdown ----------
    await mysql_connection.mysql_connection.close_connections()
    await mongo_connection.mongo_connection.close()
    logger.info("Database connections closed")


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(PracticeServiceException, practice_service_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(PracticeNotFoundException, practice_not_found_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, database_connection_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Health Check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    # Routers
    app.include_router(get_practices)

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.HOST}:{settings.PRACTICE_SERVICE_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PRACTICE_SERVICE_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )