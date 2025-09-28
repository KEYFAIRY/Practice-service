from functools import lru_cache

from app.application.use_cases.get_user_practices_use_case import GetUserPracticesUseCase
from app.domain.services.practice_metadata_service import PracticeMetadataService
from app.domain.services.practice_service import PracticeService
from app.infrastructure.repositories.mongo_metadata_repo import MongoMetadataRepository
from app.infrastructure.repositories.mysql_practice_repo import MySQLPracticeRepository


# Repositories
@lru_cache()
def get_mysql_practice_repository() -> MySQLPracticeRepository:
    """Get instance of MySQLPracticeRepository."""
    return MySQLPracticeRepository()

@lru_cache()
def get_mongo_metadata_repository() -> MongoMetadataRepository:
    """Get instance of MongoMetadataRepository."""
    return MongoMetadataRepository()

# Services
@lru_cache()
def get_practice_service() -> PracticeService:
    """Get instance of PracticeService."""
    return PracticeService(practice_repository=get_mysql_practice_repository())

@lru_cache()
def get_practice_metadata_service() -> PracticeMetadataService:
    """Get instance of PracticeMetadataService."""
    return PracticeMetadataService(metadata_repository=get_mongo_metadata_repository())

# Use Cases
@lru_cache()
def get_practices_for_user_use_case() -> GetUserPracticesUseCase:
    """Get instance of GetUserPracticesUseCase."""
    return GetUserPracticesUseCase(
        practice_service=get_practice_service(),
        practice_metadata_service=get_practice_metadata_service()
    )
    
# FastAPI Dependencies
def get_user_practices_use_case_dependency() -> GetUserPracticesUseCase:
    """Dependency for injecting GetUserPracticesUseCase."""
    return get_practices_for_user_use_case()