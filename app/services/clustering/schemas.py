from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from app.services.news.schemas import (
    ArticleResponse
)


class ClusterResponse(BaseModel):

    id: int
    title: str
    summary: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ClusterDetailResponse(
    ClusterResponse
):
    articles: list[ArticleResponse]

    model_config = ConfigDict(
        from_attributes=True
    )