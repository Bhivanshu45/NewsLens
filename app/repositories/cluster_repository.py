from sqlalchemy.orm import Session, selectinload

from app.db.models.cluster import Cluster
from app.db.models.article import Article


class ClusterRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        title: str,
    ) -> Cluster:

        cluster = Cluster(
            title=title,
        )

        self.db.add(cluster)
        self.db.flush()

        return cluster

    def get_by_id(
        self,
        cluster_id: int,
    ) -> Cluster | None:

        return (
            self.db.query(Cluster)
            .options(selectinload(Cluster.articles))
            .filter(
                Cluster.id == cluster_id
            )
            .first()
        )

    def list_clusters(self) -> list[Cluster]:
        return (
            self.db.query(Cluster)
            .order_by(Cluster.created_at.desc())
            .all()
        )


    def get_articles(
        self,
        cluster_id: int,
    ) -> list[Article]:
        cluster = self.get_by_id(cluster_id)

        if not cluster:
            return []

        return cluster.articles

    def update_summary(
        self,
        cluster: Cluster,
        summary: str,
    ) -> None:

        cluster.summary = summary

    def delete_all(self) -> int:
        return self.db.query(Cluster).delete()


    