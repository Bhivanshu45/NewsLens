from app.db.models.article import Article
from app.repositories.article_repository import ArticleRepository
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.embeddings.qdrant_service import QdrantService


class ArticleSearchService:
    def __init__(
        self,
        article_repo: ArticleRepository,
        embedding_service: EmbeddingService,
        qdrant_service: QdrantService,
    ):
        self.article_repo = article_repo
        self.embedding_service = embedding_service
        self.qdrant_service = qdrant_service

    def get_articles(
        self,
        page: int,
        limit: int,
        source: str | None,
    ) -> list[Article]:
        return self.article_repo.list_articles(page, limit, source)

    def get_article_by_id(self, article_id: int) -> Article | None:
        return self.article_repo.get_by_id(article_id)

    def search_articles(
        self,
        query: str,
        page: int,
        limit: int,
    ) -> list[Article]:
        return self.article_repo.search(query, page, limit)

    def semantic_search(
        self,
        query: str,
        limit: int,
    ) -> list[Article]:
        vector = self.embedding_service.generate_embedding(query)
        results = self.qdrant_service.search(vector=vector, limit=limit)

        article_ids = [
            result.payload["article_id"]
            for result in results.points
            if result.payload and "article_id" in result.payload
        ]

        if not article_ids:
            return []

        articles = self.article_repo.get_by_ids(article_ids)
        article_map = {article.id: article for article in articles}

        return [
            article_map[article_id]
            for article_id in article_ids
            if article_id in article_map
        ]