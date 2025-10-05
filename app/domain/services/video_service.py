import logging
from app.domain.repositories.video_repo import ILocalVideoRepository

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self, video_repository: ILocalVideoRepository):
        self.video_repository = video_repository

    async def delete_video(self, uid: str, practice_id: int) -> bool:
        logger.info(f"Deleting video for user {uid}, practice {practice_id}")
        success = await self.video_repository.delete_video(uid, practice_id)
        if success:
            logger.info(f"Successfully deleted video for user {uid}, practice {practice_id}")
        else:
            logger.warning(f"Failed to delete video for user {uid}, practice {practice_id}")
        return success