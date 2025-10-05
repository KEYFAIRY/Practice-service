from dataclasses import dataclass


@dataclass
class MusicalErrorDTO:
    id: int
    min_sec: str
    missed_note: str
    id_practice: int