from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.article_repository import ArticleRepository
from app.repositories.cluster_repository import ClusterRepository
from app.services.clustering.cluster_service import ClusterService
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.embeddings.qdrant_service import QdrantService
from app.services.llm.groq_service import GroqService
from app.services.news.ingestion_pipeline import NewsIngestionPipeline
from app.services.news.news_service import NewsService
from app.services.news.rss_service import RSSService
from app.services.search.article_search_service import ArticleSearchService


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
	return EmbeddingService()


@lru_cache(maxsize=1)
def get_groq_service() -> GroqService:
	return GroqService()


@lru_cache(maxsize=1)
def get_qdrant_service() -> QdrantService:
	return QdrantService()


def get_article_repository(db: Session = Depends(get_db)) -> ArticleRepository:
	return ArticleRepository(db)


def get_cluster_repository(db: Session = Depends(get_db)) -> ClusterRepository:
	return ClusterRepository(db)


def get_cluster_service(db: Session = Depends(get_db)) -> ClusterService:
	return ClusterService(
		article_repo=get_article_repository(db),
		cluster_repo=get_cluster_repository(db),
		qdrant_service=get_qdrant_service(),
		groq_service=get_groq_service(),
	)


def get_news_ingestion_pipeline(db: Session = Depends(get_db)) -> NewsIngestionPipeline:
	return NewsIngestionPipeline(
		article_repo=get_article_repository(db),
		embedding_service=get_embedding_service(),
		groq_service=get_groq_service(),
		cluster_service=get_cluster_service(db),
	)


def get_news_service(db: Session = Depends(get_db)) -> NewsService:
	return NewsService(
		db=db,
		rss_service=RSSService(),
		pipeline=get_news_ingestion_pipeline(db),
	)


def get_article_search_service(db: Session = Depends(get_db)) -> ArticleSearchService:
	return ArticleSearchService(
		article_repo=get_article_repository(db),
		embedding_service=get_embedding_service(),
		qdrant_service=get_qdrant_service(),
	)


__all__ = [
	"get_db",
	"get_embedding_service",
	"get_groq_service",
	"get_qdrant_service",
	"get_article_repository",
	"get_cluster_repository",
	"get_cluster_service",
	"get_news_ingestion_pipeline",
	"get_news_service",
	"get_article_search_service",
]