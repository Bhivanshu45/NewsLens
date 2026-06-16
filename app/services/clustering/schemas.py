from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ClusterResponse(BaseModel):

    id: int
    title: str
    summary: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )