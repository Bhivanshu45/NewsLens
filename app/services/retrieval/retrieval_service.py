from app.repositories.article_repository import ArticleRepository
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.embeddings.qdrant_service import QdrantService

from app.services.retrieval.schemas import RetrievedArticle


class RetrievalService:

	def __init__(
		self,
		article_repo: ArticleRepository,
		embedding_service: EmbeddingService,
		qdrant_service: QdrantService,
	):
		self.article_repo = article_repo
		self.embedding_service = embedding_service
		self.qdrant_service = qdrant_service

	def retrieve(
		self,
		query: str,
		limit: int = 5,
	) -> list[RetrievedArticle]:
		vector = self.embedding_service.generate_embedding(query)
		results = self.qdrant_service.search(
			vector=vector,
			limit=limit,
		)

		ranked_matches: list[tuple[int, float]] = []
		article_ids: list[int] = []

		for result in results.points:
			payload = result.payload or {}
			article_id = payload.get("article_id")

			if article_id is None:
				continue

			ranked_matches.append(
				(article_id, result.score)
			)
			article_ids.append(article_id)

		if not article_ids:
			return []

		articles = self.article_repo.get_by_ids(article_ids)
		article_map = {article.id: article for article in articles}

		retrieved_articles: list[RetrievedArticle] = []

		for article_id, score in ranked_matches:
			article = article_map.get(article_id)

			if article is None:
				continue

			retrieved_articles.append(
				RetrievedArticle(
					article=article,
					score=score,
				)
			)

		return retrieved_articles
