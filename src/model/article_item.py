from pydantic import BaseModel
from typing import List
from .ai_response import AIResponse

class ArticleItem(BaseModel):
    title: str
    link: str

    content: str | None = None
    comments: List[str] | None = None
    audio_path: str | None = None
    summary: AIResponse | None = None

    def __str__(self) -> str:
        return f'title: {self.title}\nlink: {self.link}'
