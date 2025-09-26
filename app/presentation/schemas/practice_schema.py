from typing import List
from pydantic import BaseModel, Field

class PracticeItem(BaseModel):
    """Single practice entry"""
    practice_id: int = Field(..., description="Practice ID", example=26)
    scale: str = Field(..., description="Scale practiced", example="C Major")
    scale_type: str = Field(..., description="Scale type", example="Major")
    date: str = Field(..., description="Date of the practice", example="2023-10-01")
    time: str = Field(..., description="Time of the practice", example="15:30:00")
    state: str = Field(..., description="Status of the practice", example="completed")
    
class PracticeResponse(BaseModel):
    """Response with information about a registered practice"""
    num_practices: int = Field(..., description="Number of practices retrieved", example=5)
    practices: List[PracticeItem] = Field(..., description="List of practices", example=[])
    
    class Config:
        schema_extra = {
            "example": {
                "num_practices": 5,
                "practices": [
                    {
                        "practice_id": "26",
                        "scale": "C Major",
                        "scale_type": "Major",
                        "date": "2023-10-01",
                        "time": "15:30:00",
                        "state": "completed",
                    },
                    # More practice items...
                ]
            }
        }