from app.db.session import SessionLocal

from app.db.models.article import Article
from app.db.models.cluster import Cluster


def reset_clusters():
    db = SessionLocal()

    try:

        updated = (
            db.query(Article)
            .update(
                {
                    Article.cluster_id: None
                }
            )
        )

        deleted = (
            db.query(Cluster)
            .delete()
        )

        db.commit()

        print(
            f"Reset complete.\n"
            f"Articles updated: {updated}\n"
            f"Clusters deleted: {deleted}"
        )

    except Exception as e:

        db.rollback()

        print(
            f"Reset failed: {e}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    reset_clusters()