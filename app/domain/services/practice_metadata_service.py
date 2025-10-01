import logging
from app.domain.entities.practice import Practice
from app.domain.entities.practice_metadata import PracticeMetadata
from app.domain.repositories.metadata_repo import IMetaDataRepository

logger = logging.getLogger(__name__)

class PracticeMetadataService:
    """Service for managing practice metadata."""

    def __init__(self, metadata_repository: IMetaDataRepository):
        self.metadata_repository = metadata_repository
        
    async def get_practice_metadata(self, uid: str, practice_id: int) -> PracticeMetadata:
        logger.debug(f"Service fetching metadata for uid={uid}, practice_id={practice_id}")
        return await self.metadata_repository.get_practice_metadata(uid, practice_id)
    
    async def finish_practice(self, uid: str, practice_id: int) -> PracticeMetadata:
        logger.debug(f"Service finishing practice for uid={uid}, practice_id={practice_id}")
        return await self.metadata_repository.finish_practice(uid, practice_id)