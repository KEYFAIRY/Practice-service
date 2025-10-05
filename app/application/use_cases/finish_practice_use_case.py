from app.application.dto.practice_metadata_dto import PracticeMetadataDTO
from app.domain.services.practice_metadata_service import PracticeMetadataService
from app.domain.services.video_service import VideoService


class FinishPracticeUseCase:
    def __init__(self, practice_metadata_service: PracticeMetadataService, video_service: VideoService):
        self.practice_metadata_service = practice_metadata_service
        self.video_service = video_service

    async def execute(self, uid: str, practice_id: int) -> PracticeMetadataDTO:
        # Delete video
        await self.video_service.delete_video(uid, practice_id)
        
        # Update metadata
        return await self.practice_metadata_service.finish_practice(uid, practice_id)