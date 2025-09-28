from dataclasses import dataclass


@dataclass
class PracticeDTO:
    id: int
    scale: str
    scale_type: str
    date: str
    time: str
    state: str
    local_video_url: str
    pdf_url: str