from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, ConfigDict

@dataclass
class ParsedArticle:
    title: str
    content: str
    source: str
    url: str
    published_at: datetime | None



class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str | None
    source: str
    url: str
    published_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )