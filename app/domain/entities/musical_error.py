from dataclasses import dataclass

@dataclass
class MusicalError:
    id: int
    min_sec: str
    missed_note: str
    id_practice: int