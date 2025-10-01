from typing import List
from pydantic import BaseModel

class PosturalErrorItem(BaseModel):
    min_sec_init: str
    min_sec_end: str
    explication: str


class PosturalErrorResponse(BaseModel):
    num_errors: int
    errors: List[PosturalErrorItem]