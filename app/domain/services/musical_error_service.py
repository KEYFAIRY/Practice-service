import logging
from typing import List
from app.domain.entities.musical_error import MusicalError
from app.domain.repositories.musical_errror_repo import IMusicalErrorRepository


logger = logging.getLogger(__name__)

class MusicalErrorService:
    def __init__(self, musical_error_repo: IMusicalErrorRepository):
        self.musical_error_repo = musical_error_repo

    async def get_musical_errors_by_practice(self, practice_id: int) -> List[MusicalError]:
        logger.debug(f"Fetching musical errors for practice ID: {practice_id}")
        return await self.musical_error_repo.get_musical_errors_by_practice_id(practice_id)