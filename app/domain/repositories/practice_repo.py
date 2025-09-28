from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from app.domain.entities.practice import Practice


class IPracticeRepository(ABC):
    
    @abstractmethod
    async def get_practices_for_user(self, uid: str, last_id: Optional[int] = None) -> List[Practice]:
        pass