from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.core.constants import EMBEDDING_DIMENSION, QDRANT_COLLECTION, QDRANT_SEARCH_LIMIT


class QdrantService:

    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url
        )
        self._collection_ready = False

    def _ensure_collection(self):
        if self._collection_ready:
            return

        collections = self.client.get_collections()

        existing = [
            collection.name
            for collection in collections.collections
        ]

        if QDRANT_COLLECTION not in existing:
            self.client.create_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )

        self._collection_ready = True

    def create_collection(self):
        self._ensure_collection()


    def upsert_article(
        self,
        article_id: int,
        vector: list[float],
        payload: dict,
    ):
        self._ensure_collection()

        self.client.upsert(
            collection_name=QDRANT_COLLECTION,
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
        limit: int = QDRANT_SEARCH_LIMIT,
    ):
        self._ensure_collection()

        return self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=vector,
            limit=limit,
        )