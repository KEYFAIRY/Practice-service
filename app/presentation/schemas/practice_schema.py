from typing import List
from pydantic import BaseModel, Field

class PracticeItem(BaseModel):
    """Single practice entry"""
    practice_id: int = Field(..., description="Practice ID", example=26)
    scale: str = Field(..., description="Scale practiced", example="C Major")
    scale_type: str = Field(..., description="Scale type", example="Major")
    duration: int = Field(..., description="Duration of the practice in seconds", example=300)
    bpm: int = Field(..., description="Beats per minute", example=120)
    figure: str = Field(..., description="Figure practiced", example="Negra")
    octaves: int = Field(..., description="Number of octaves practiced", example=2)
    date: str = Field(..., description="Date of the practice", example="2023-10-01")
    time: str = Field(..., description="Time of the practice", example="15:30:00")
    state: str = Field(..., description="Status of the practice", example="completed")
    local_video_url: str = Field(None, description="URL to the local video of the practice", example="http://example.com/video.mp4")
    pdf_url: str = Field(None, description="URL to the PDF of the practice", example="http://example.com/sheet.pdf")
    
    
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
                        "duration": 300,
                        "bpm": 120,
                        "figure": "Negra",
                        "octaves": 2,
                        "date": "2023-10-01",
                        "time": "15:30:00",
                        "state": "completed",
                        "local_video_url": "http://example.com/video.mp4",
                        "pdf_url": "http://example.com/sheet.pdf"
                    },
                    # More practice items...
                ]
            }
        }