from app.core.logger import logger
from app.db.models.article import Article
from app.db.models.cluster import Cluster

from app.repositories.article_repository import (
    ArticleRepository,
)

from app.repositories.cluster_repository import (
    ClusterRepository,
)

from app.services.embeddings.qdrant_service import (
    QdrantService,
)

from app.services.llm.groq_service import (
    GroqService,
)

from app.core.constants import (
    QDRANT_SEARCH_LIMIT,
    SIMILARITY_THRESHOLD,
)


class ClusterService:

    def __init__(
        self,
        article_repo: ArticleRepository,
        cluster_repo: ClusterRepository,
        qdrant_service: QdrantService,
        groq_service: GroqService,
    ):

        self.article_repo = article_repo
        self.cluster_repo = cluster_repo
        self.qdrant_service = qdrant_service
        self.groq_service = groq_service

    def list_clusters(self) -> list:
        return self.cluster_repo.list_clusters()

    def get_cluster_by_id(self, cluster_id: int) -> Cluster | None:
        return self.cluster_repo.get_by_id(cluster_id)

    def cluster_article(
        self,
        article: Article,
        vector: list[float],
    ) -> int:

        payload = {
            "article_id": article.id,
            "title": article.title,
            "source": article.source,
            "url": article.url,
        }

        self.qdrant_service.upsert_article(
            article_id=article.id,
            vector=vector,
            payload=payload,
        )

        results = self.qdrant_service.search(
            vector=vector,
            limit=QDRANT_SEARCH_LIMIT,
        )

        similar_article = None
        similarity_score = None

        for result in results.points:

            payload = result.payload

            if payload["article_id"] == article.id:
                continue

            similar_article = (
                self.article_repo.get_by_id(
                    payload["article_id"]
                )
            )

            similarity_score = result.score

            break

        cluster_id = self.assign_cluster(
            article=article,
            similar_article=similar_article,
            similarity_score=similarity_score,
        )

        self.article_repo.update_cluster(
            article,
            cluster_id,
        )

        self.generate_cluster_summary(
            cluster_id
        )

        return cluster_id

    def assign_cluster(
        self,
        article: Article,
        similar_article: Article | None,
        similarity_score: float | None,
    ) -> int:

        if (
            similar_article
            and similarity_score is not None
            and similarity_score >= SIMILARITY_THRESHOLD
        ):

            if similar_article.cluster_id:

                return similar_article.cluster_id

            cluster = self.cluster_repo.create(
                similar_article.title
            )

            self.article_repo.update_cluster(
                similar_article,
                cluster.id,
            )

            return cluster.id

        cluster = self.cluster_repo.create(
            article.title
        )

        return cluster.id

    def generate_cluster_summary(
        self,
        cluster_id: int,
    ) -> None:

        articles = (
            self.cluster_repo.get_articles(
                cluster_id
            )
        )

        if len(articles) < 2:
            return

        text = "\n\n".join(
            article.summary or article.title
            for article in articles
        )

        summary = (
            self.groq_service
            .generate_cluster_summary(
                text
            )
        )

        cluster = (
            self.cluster_repo.get_by_id(
                cluster_id
            )
        )

        if not cluster:
            logger.warning("Cluster %s not found while updating summary", cluster_id)
            return

        self.cluster_repo.update_summary(
            cluster,
            summary,
        )