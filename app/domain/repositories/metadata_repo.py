from abc import ABC, abstractmethod

from app.domain.entities.practice_metadata import PracticeMetadata


class IMetaDataRepository(ABC):
    """Abstract base class for metadata repository.""" 
    
    @abstractmethod
    async def get_practice_metadata(self, uid: str, practice_id: int) -> PracticeMetadata:
        pass
    
    @abstractmethod
    async def finish_practice(self, uid: str, practice_id: int) -> PracticeMetadata:
        pass