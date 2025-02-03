from pydantic import BaseModel
from typing import List


class AIResponse(BaseModel):
    summary: str
    keywords: List[str]
    controversy_level: str
