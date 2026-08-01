from app.db.session import SessionLocal

from app.core.logger import logger
from app.core.providers import get_cluster_service, get_embedding_service

from app.repositories.article_repository import ArticleRepository


def backfill_clusters():

    db = SessionLocal()

    article_repo = ArticleRepository(db)
    embedding_service = get_embedding_service()
    cluster_service = get_cluster_service(db)

    try:
        articles = article_repo.list_unclustered()

        logger.info("Found %s unclustered articles", len(articles))

        for article in articles:

            vector = embedding_service.generate_article_embedding(article)

            cluster_id = cluster_service.cluster_article(
                article=article,
                vector=vector,
            )

            logger.info("Article %s -> Cluster %s", article.id, cluster_id)

        db.commit()

        logger.info("Cluster backfill completed")

    except Exception:

        db.rollback()

        logger.exception("Backfill failed")

    finally:
        db.close()


if __name__ == "__main__":
    backfill_clusters()