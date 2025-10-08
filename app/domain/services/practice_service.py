from datetime import date
import logging
from typing import List, Optional

from app.domain.entities.practice import Practice
from app.domain.repositories.practice_repo import IPracticeRepository

logger = logging.getLogger(__name__)

class PracticeService:
    """Service for managing practices."""
    
    def __init__ (self, practice_repository: IPracticeRepository):
        self.practice_repository = practice_repository

    async def get_practices_for_user(self, uid: str, last_id: Optional[int] = None, limit: Optional[int] = None) -> List[Practice]:
        logger.debug(f"Service fetching practices for uid={uid}, last_id={last_id}, limit={limit}")
        return await self.practice_repository.get_practices_for_user(uid, last_id, limit)
    
    async def get_practice_by_id(self, uid: str, practice_id: int) -> Practice:
        logger.debug(f"Service getting practice for uid={uid} and practice id={practice_id}")
        return await self.practice_repository.get_practice_by_id(uid, practice_id)