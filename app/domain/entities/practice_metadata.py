from dataclasses import dataclass


@dataclass
class PracticeMetadata:
    id_practice: int
    video_in_local: str
    report: str
    video_done: bool
    audio_done: bool