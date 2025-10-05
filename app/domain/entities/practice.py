from dataclasses import dataclass


@dataclass
class Practice:
    id: int
    scale: str
    scale_type: str
    duration: int
    bpm: int
    figure: float
    octaves: int
    date: str
    time: str
    state: str
    local_video_url: str
    pdf_url: str
