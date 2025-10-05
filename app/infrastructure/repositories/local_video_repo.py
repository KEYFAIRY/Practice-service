import logging
import os

from app.domain.repositories.video_repo import ILocalVideoRepository

logger = logging.getLogger(__name__)

class LocalVideoRepository(ILocalVideoRepository):
    """Concrete implementation of ILocalVideoRepository using local filesystem."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or os.getenv("CONTAINER_PATH", "/app/storage")

    async def delete_video(self, uid: str, practice_id: int) -> bool:
        """Delete a video file if it exists."""
        file_path = os.path.join(self.base_dir, uid, "videos", f"practice_{practice_id}.mp4")
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Video deleted: {file_path}")
                return True
            else:
                logger.warning(f"Video not found for deletion: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting video {file_path}: {e}")
            return False