from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
)

from app.core.config import settings
from qdrant_client.models import PointStruct


class QdrantService:

    COLLECTION_NAME = "news_articles"

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url
        )

    def create_collection(self):

        collections = (
            self.client.get_collections()
        )

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME in existing:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


    def upsert_article(
        self,
        article_id: int,
        vector: list[float],
        payload: dict,
    ):
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=article_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )


    def search(
        self,
        vector: list[float],
        limit: int = 5,
    ):
        return self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=vector,
            limit=limit,
        )