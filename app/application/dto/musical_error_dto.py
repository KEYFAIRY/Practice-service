from dataclasses import dataclass


@dataclass
class MusicalErrorDTO:
    id: int
    min_sec: str
    note_played: str
    note_correct: str
    id_practice: int