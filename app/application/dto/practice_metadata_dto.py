@dataclass
class PracticeMetadataDTO:
    id_practice: int
    video_in_local: str
    report: str
    video_done: bool
    audio_done: bool

    