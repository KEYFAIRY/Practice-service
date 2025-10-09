from typing import List
from pydantic import BaseModel, Field


class MusicalErrorItem(BaseModel):
    """Single musical error entry"""

    min_sec: str = Field(..., description="Timestamp of the error (mm:ss)", example="00:12")
    note_played: str = Field(..., description="Note that was played", example="D")
    note_correct: str = Field(..., description="Correct note that should have been played", example="D")


class MusicalErrorResponse(BaseModel):
    """Response with information about musical errors in a practice"""

    num_errors: int = Field(..., description="Number of musical errors detected", example=3)
    errors: List[MusicalErrorItem] = Field(..., description="List of musical errors detected", example=[])

    class Config:
        schema_extra = {
            "example": {
                "num_errors": 3,
                "errors": [
                    {
                        "min_sec": "00:12",
                        "missed_note": "C#",
                    },
                    {
                        "min_sec": "00:24",
                        "missed_note": "F",
                    },
                    {
                        "min_sec": "00:36",
                        "missed_note": "G",
                    }
                ]
            }
        }