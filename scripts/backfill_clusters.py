from app.db.session import SessionLocal

from app.db.models.article import Article

from app.services.embeddings.embedding_service import (
    EmbeddingService,
)

from app.services.embeddings.qdrant_service import (
    QdrantService,
)

from app.services.clustering.cluster_service import (
    ClusterService,
)


def backfill_clusters():

    db = SessionLocal()

    embedding_service = EmbeddingService()
    qdrant_service = QdrantService()

    cluster_service = ClusterService(db)

    try:

        articles = (
            db.query(Article)
            .order_by(Article.id.asc())
            .limit(10)  # Debugging ke liye
            .all()
        )

        print(
            f"Found {len(articles)} articles"
        )

        for article in articles:

            if article.cluster_id:
                continue

            text = f"""
            Title:
            {article.title}

            Summary:
            {article.summary or ''}

            Content:
            {article.content}
            """

            vector = (
                embedding_service
                .generate_embedding(text)
            )

            search_results = (
                qdrant_service.search(
                    vector=vector,
                    limit=5,
                )
            )

            similar_article = None
            similarity_score = None

            for result in search_results.points:

                payload = result.payload

                # Skip self
                if (
                    payload["article_id"]
                    == article.id
                ):
                    continue

                similar_article = (
                    db.query(Article)
                    .filter(
                        Article.id ==
                        payload["article_id"]
                    )
                    .first()
                )

                if not similar_article:
                    continue

                similarity_score = result.score

                break

            print(
                f"Article={article.id}, "
                f"Similar={similar_article.id if similar_article else None}, "
                f"Score={similarity_score}"
            )

            cluster_id = (
                cluster_service.assign_cluster(
                    article=article,
                    similar_article=similar_article,
                    similarity_score=similarity_score,
                )
            )

            article.cluster_id = cluster_id

            print(
                f"Article {article.id} "
                f"-> Cluster {cluster_id}"
            )

        db.commit()

        print(
            "Cluster backfill completed"
        )

    except Exception as e:

        db.rollback()

        print(
            f"Backfill failed: {e}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    backfill_clusters()