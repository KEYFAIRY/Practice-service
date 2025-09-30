from abc import ABC, abstractmethod


class IReportRepository(ABC):
    @abstractmethod
    async def get_pdf(self, uid: str, practice_id: int) -> bytes:
        pass