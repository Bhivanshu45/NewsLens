from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.db.models.cluster import Cluster
from app.services.llm.groq_service import GroqService


class ClusterService:

    # V1 threshold
    SIMILARITY_THRESHOLD = 0.70

    def __init__(self, db: Session):
        self.db = db

    def create_cluster(
        self,
        title: str,
    ) -> Cluster:

        cluster = Cluster(
            title=title,
        )

        self.db.add(cluster)

        # cluster.id generate karwane ke liye
        self.db.flush()

        return cluster

    def assign_cluster(
        self,
        article: Article,
        similar_article: Article | None,
        similarity_score: float | None,
    ) -> int:

        # Similar article mila aur score threshold cross karta hai
        if (
            similar_article
            and similarity_score is not None
            and similarity_score >= self.SIMILARITY_THRESHOLD
        ):

            # Similar article pehle se kisi cluster me hai
            if similar_article.cluster_id:
                return similar_article.cluster_id

            # Similar article ka cluster nahi hai
            # To uske naam se cluster create karo
            cluster = self.create_cluster(
                title=similar_article.title
            )

            similar_article.cluster_id = cluster.id

            return cluster.id

        # Koi suitable cluster nahi mila
        # Naya cluster create karo
        cluster = self.create_cluster(
            title=article.title
        )

        return cluster.id


    def get_cluster_by_id(
        self,
        cluster_id: int,
    ):
        return (
            self.db.query(Cluster)
            .filter(
                Cluster.id == cluster_id
            )
            .first()
        )


    def generate_cluster_summary(
        self,
        cluster_id: int,
    ):
        cluster = (
            self.db.query(Cluster)
            .filter(
                Cluster.id == cluster_id
            )
            .first()
        )

        if not cluster:
            return

        articles = cluster.articles

        if len(articles) < 2:
            return

        text = "\n\n".join(
            article.summary or article.title
            for article in articles
        )

        summary = (
            GroqService()
            .generate_cluster_summary(text)
        )

        cluster.summary = summary