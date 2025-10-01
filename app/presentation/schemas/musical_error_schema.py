from typing import List
from pydantic import BaseModel

class MusicalErrorItem(BaseModel):
    min_sec: str
    note_played: str
    note_correct: str


class MusicalErrorResponse(BaseModel):
    num_errors: int
    errors: List[MusicalErrorItem]