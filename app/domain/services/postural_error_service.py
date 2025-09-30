from typing import List

from flask import logging
from app.domain.entities.postural_error import PosturalError
from app.domain.repositories.postural_error_repo import IPosturalErrorRepository


logger = logging.getLogger(__name__)

class PosturalErrorService:
    def __init__(self, postural_error_repo: IPosturalErrorRepository):
        self.postural_error_repo = postural_error_repo

    async def get_postural_errors_by_practice_id(self, practice_id: int) -> List[PosturalError]:
        logger.debug(f"Fetching postural errors for practice ID: {practice_id}")
        return await self.postural_error_repo.get_postural_errors_by_practice_id(practice_id)