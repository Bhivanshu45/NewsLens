from app.db.session import SessionLocal

from app.core.logger import logger
from app.repositories.article_repository import ArticleRepository
from app.repositories.cluster_repository import ClusterRepository


def reset_clusters():
    db = SessionLocal()
    article_repo = ArticleRepository(db)
    cluster_repo = ClusterRepository(db)

    try:
        updated = article_repo.clear_clusters()
        deleted = cluster_repo.delete_all()

        db.commit()

        logger.info(
            "Reset complete. articles_updated=%s clusters_deleted=%s",
            updated,
            deleted,
        )

    except Exception:

        db.rollback()

        logger.exception("Reset failed")

    finally:
        db.close()


if __name__ == "__main__":
    reset_clusters()