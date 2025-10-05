from abc import ABC, abstractmethod


class ILocalVideoRepository(ABC):
    @abstractmethod
    async def delete_video(self, uid: str, practice_id: int) -> bool:
        pass