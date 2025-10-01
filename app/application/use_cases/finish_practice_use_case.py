from app.application.dto.practice_metadata_dto import PracticeMetadataDTO
from app.domain.services.practice_metadata_service import PracticeMetadataService


class FinishPracticeUseCase:
    def __init__(self, practice_metadata_service: PracticeMetadataService):
        self.practice_metadata_service = practice_metadata_service
        
    async def execute(self, uid: str, practice_id: int) -> PracticeMetadataDTO:
        return await self.practice_metadata_service.finish_practice(uid, practice_id)