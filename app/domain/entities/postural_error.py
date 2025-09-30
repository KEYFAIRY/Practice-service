from dataclasses import dataclass

@dataclass
class PosturalError:
    id: int
    min_sec_init: str
    min_sec_end: int
    explication: str
    id_practice: int