from app.core.logger import logger
from app.repositories.article_repository import ArticleRepository
from app.services.clustering.cluster_service import ClusterService
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.llm.groq_service import GroqService
from app.services.news.schemas import ParsedArticle


class NewsIngestionPipeline:

    def __init__(
        self,
        article_repo: ArticleRepository,
        embedding_service: EmbeddingService,
        groq_service: GroqService,
        cluster_service: ClusterService,
    ):

        self.article_repo = article_repo

        self.embedding_service = embedding_service

        self.groq_service = groq_service

        self.cluster_service = cluster_service

    def process_article(
        self,
        article: ParsedArticle,
    ) -> bool:
        try:
            if self.article_repo.exists(
                article.url,
            ):
                return False

            summary = self.summarize_article(
                article.content,
            )

            db_article = self.save_article(article, summary)

            vector = self.embed_article(
                db_article,
            )

            self.cluster_article(
                db_article,
                vector,
            )

            return True

        except Exception:
            logger.exception(
                "Failed to process article %s",
                getattr(article, "url", "unknown"),
            )

            return False

    def summarize_article(
        self,
        content: str,
    ) -> str | None:

        if not content:
            return None

        try:

            logger.info(
                "Generating article summary..."
            )

            return (
                self.groq_service
                .generate_summary(
                    content
                )
            )

        except Exception:

            logger.exception(
                "Failed to generate summary."
            )

            return None

    def save_article(
        self,
        article: ParsedArticle,
        summary: str | None,
    ):
        return self.article_repo.create_from_parsed_article(
            article,
            summary,
        )


    def embed_article(
        self,
        article,
    ) -> list[float]:

        logger.info(
            "Generating article embedding..."
        )

        return (
            self.embedding_service
            .generate_article_embedding(
                article
            )
        )

    def cluster_article(
        self,
        article,
        vector: list[float],
    ) -> int:

        logger.info(
            "Assigning article to cluster..."
        )

        try:

            cluster_id = (
                self.cluster_service
                .cluster_article(
                    article=article,
                    vector=vector,
                )
            )

            logger.info(
                f"Article assigned to cluster {cluster_id}"
            )

            return cluster_id

        except Exception:

            logger.exception(
                "Failed to cluster article."
            )

            raise