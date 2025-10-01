from typing import List
from pydantic import BaseModel, Field


class PosturalErrorItem(BaseModel):
    """Single postural error entry"""

    min_sec_init: str = Field(..., description="Start time of the error (mm:ss)", example="00:05")
    min_sec_end: str = Field(..., description="End time of the error (mm:ss)", example="00:12")
    explication: str = Field(..., description="Explanation of the detected postural error", example="Incorrect wrist position")


class PosturalErrorResponse(BaseModel):
    """Response with information about postural errors in a practice"""

    num_errors: int = Field(..., description="Number of postural errors detected", example=2)
    errors: List[PosturalErrorItem] = Field(..., description="List of postural errors detected", example=[])

    class Config:
        schema_extra = {
            "example": {
                "num_errors": 2,
                "errors": [
                    {
                        "min_sec_init": "00:05",
                        "min_sec_end": "00:12",
                        "explication": "Incorrect wrist position"
                    },
                    {
                        "min_sec_init": "00:20",
                        "min_sec_end": "00:25",
                        "explication": "Shoulders raised during scale execution"
                    }
                ]
            }
        }