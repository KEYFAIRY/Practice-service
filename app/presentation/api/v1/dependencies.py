from functools import lru_cache

from app.application.use_cases.finish_practice_use_case import FinishPracticeUseCase
from app.application.use_cases.get_musical_errors_use_case import GetMusicalErrorsUseCase
from app.application.use_cases.get_postural_errors_use_case import GetPosturalErrorsUseCase
from app.application.use_cases.get_report_use_case import GetReportUseCase
from app.application.use_cases.get_user_practices_use_case import GetUserPracticesUseCase
from app.domain.services.musical_error_service import MusicalErrorService
from app.domain.services.postural_error_service import PosturalErrorService
from app.domain.services.practice_metadata_service import PracticeMetadataService
from app.domain.services.practice_service import PracticeService
from app.domain.services.report_service import ReportService
from app.infrastructure.repositories.local_report_repo import LocalReportRepository
from app.infrastructure.repositories.mongo_metadata_repo import MongoMetadataRepository
from app.infrastructure.repositories.mysql_musical_error_repo import MySQLMusicalErrorRepository
from app.infrastructure.repositories.mysql_postural_error_repo import MySQLPosturalErrorRepository
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

@lru_cache
def get_local_report_repository() -> LocalReportRepository:
    """Get instance of LocalReportRepository."""
    return LocalReportRepository()

@lru_cache()
def get_postural_error_repository() -> MySQLPosturalErrorRepository:
    """Get instance of MySQLPosturalErrorRepository."""
    return MySQLPosturalErrorRepository()

@lru_cache()
def get_musical_error_repository() -> MySQLMusicalErrorRepository:
    """Get instance of MySQLMusicalErrorRepository."""
    return MySQLMusicalErrorRepository()

# Services
@lru_cache()
def get_practice_service() -> PracticeService:
    """Get instance of PracticeService."""
    return PracticeService(practice_repository=get_mysql_practice_repository())

@lru_cache()
def get_practice_metadata_service() -> PracticeMetadataService:
    """Get instance of PracticeMetadataService."""
    return PracticeMetadataService(metadata_repository=get_mongo_metadata_repository())

@lru_cache()
def get_report_service() -> ReportService:
    """Get instance of ReportService."""
    return ReportService(report_repository=get_local_report_repository())

@lru_cache()
def get_postural_error_service() -> PosturalErrorService:
    """Get instance of PosturalErrorService."""
    return PosturalErrorService(postural_error_repo=get_postural_error_repository())

@lru_cache()
def get_musical_error_service() -> MusicalErrorService:
    """Get instance of MusicalErrorService."""
    return MusicalErrorService(musical_error_repo=get_musical_error_repository())

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
    
@lru_cache()
def get_report_use_case() -> GetReportUseCase:
    """Get instance of GetReportUseCase."""
    return GetReportUseCase(report_service=get_report_service())

@lru_cache()
def get_postural_errors_use_case() -> GetPosturalErrorsUseCase:
    """Get instance of GetPosturalErrorsUseCase."""
    return GetPosturalErrorsUseCase(postural_error_service=get_postural_error_service())

@lru_cache()
def get_musical_errors_use_case() -> GetMusicalErrorsUseCase:
    """Get instance of GetMusicalErrorsUseCase."""
    return GetMusicalErrorsUseCase(musical_error_service=get_musical_error_service())

@lru_cache()
def get_finish_practice_use_case() -> FinishPracticeUseCase:
    """Get instance of FinishPracticeUseCase."""
    return FinishPracticeUseCase(practice_metadata_service=get_practice_metadata_service())
    
# FastAPI Dependencies
def get_user_practices_use_case_dependency() -> GetUserPracticesUseCase:
    """Dependency for injecting GetUserPracticesUseCase."""
    return get_practices_for_user_use_case()

def get_report_use_case_dependency() -> GetReportUseCase:
    """Dependency for injecting GetReportUseCase."""
    return get_report_use_case()

def get_postural_errors_use_case_dependency() -> GetPosturalErrorsUseCase:
    """Dependency for injecting GetPosturalErrorsUseCase."""
    return get_postural_errors_use_case()

def get_musical_errors_use_case_dependency() -> GetMusicalErrorsUseCase:
    """Dependency for injecting GetMusicalErrorsUseCase."""
    return get_musical_errors_use_case()

def get_finish_practice_use_case_dependency() -> FinishPracticeUseCase:
    """Dependency for injecting FinishPracticeUseCase."""
    return get_finish_practice_use_case()