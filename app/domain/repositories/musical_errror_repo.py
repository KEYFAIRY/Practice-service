from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.musical_error import MusicalError


class IMusicalErrorRepository(ABC): 
    
    @abstractmethod
    async def get_musical_errors_by_practice_id(self, practice_id: int) -> List[MusicalError]:
        pass