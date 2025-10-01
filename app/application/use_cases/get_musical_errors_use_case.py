from typing import List

from app.application.dto.musical_error_dto import MusicalErrorDTO
from app.domain.services.musical_error_service import MusicalErrorService


class GetMusicalErrorsUseCase:
    def __init__(self, musical_error_service: MusicalErrorService):
        self.musical_error_service = musical_error_service

    async def execute(self, practice_id: int) -> List[MusicalErrorDTO]:
        musical_errors = await self.musical_error_service.get_musical_errors_by_practice(practice_id)
        return [MusicalErrorDTO(
            id=error.id,
            min_sec=error.min_sec,
            note_played=error.note_played,
            note_correct=error.note_correct,
            id_practice=error.id_practice
        ) for error in musical_errors]