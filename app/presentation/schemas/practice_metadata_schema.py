from pydantic import BaseModel, Field


class PracticeMetadataResponse(BaseModel):
    """Metadata of a finished practice"""

    id_practice: int = Field(..., description="Practice ID", example=26)
    video_in_local: str = Field("", description="Local video path, cleared when practice is finished", example="")
    report: str = Field(None, description="Report generated for the practice", example="Good progress, posture improved")
    video_done: bool = Field(..., description="Whether the video processing is completed", example=True)
    audio_done: bool = Field(..., description="Whether the audio processing is completed", example=True)

    class Config:
        schema_extra = {
            "example": {
                "id_practice": 26,
                "video_in_local": "",
                "report": "Good progress, posture improved",
                "video_done": True,
                "audio_done": True
            }
        }
