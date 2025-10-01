from typing import List
from app.application.dto.postural_error_dto import PosturalErrorDTO
from app.domain.services.postural_error_service import PosturalErrorService


class GetPosturalErrorsUseCase:
    def __init__(self, postural_error_service: PosturalErrorService):
        self.postural_error_service = postural_error_service

    async def execute(self, practice_id: int) -> List[PosturalErrorDTO]:
        potural_errors = await self.postural_error_service.get_postural_errors_by_practice_id(practice_id)
        return [PosturalErrorDTO(
            min_sec_init=error.min_sec_init,
            min_sec_end=error.min_sec_end,
            explication=error.explication,
        ) for error in potural_errors]