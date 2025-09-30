from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.postural_error import PosturalError


class IPosturalErrorRepository(ABC): 
    
    @abstractmethod
    async def get_postural_errors_by_practice_id(self, practice_id: int) -> List[PosturalError]:
        pass