from app.db.models.article import Article
from app.repositories.article_repository import ArticleRepository
from app.services.retrieval.retrieval_service import RetrievalService


class ArticleSearchService:
    def __init__(
        self,
        article_repo: ArticleRepository,
        retrieval_service: RetrievalService,
    ):
        self.article_repo = article_repo
        self.retrieval_service = retrieval_service

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
        retrieved_articles = self.retrieval_service.retrieve(
            query=query,
            limit=limit,
        )

        return [
            retrieved_article.article
            for retrieved_article in retrieved_articles
        ]