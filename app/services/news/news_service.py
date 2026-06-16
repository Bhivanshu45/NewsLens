from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.services.news.rss_service import RSSService
from app.services.llm.groq_service import GroqService

from app.services.embeddings.embedding_service import (
    EmbeddingService,
)

from app.services.embeddings.qdrant_service import (
    QdrantService,
)
from app.services.clustering.cluster_service import (
    ClusterService,
)


class NewsService:
    def __init__(self, db: Session):
        self.db = db

        self.rss_service = RSSService()
        self.groq_service = GroqService()

        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

        self.cluster_service = ClusterService(db)

    def ingest_articles(self):
        articles = self.rss_service.fetch_and_parse_feeds()

        inserted = 0
        skipped = 0

        for article in articles:

            existing_article = (
                self.db.query(Article)
                .filter(Article.url == article.url)
                .first()
            )

            if existing_article:
                skipped += 1
                continue

            summary = None

            print(
                f"Generating summary for: {article.title}"
            )

            try:
                if article.content:
                    summary = (
                        self.groq_service
                        .generate_summary(
                            article.content
                        )
                    )

            except Exception as e:
                print(
                    f"Summary generation failed: {e}"
                )

            article_data = Article(
                title=article.title,
                content=article.content,
                summary=summary,
                source=article.source,
                url=article.url,
                published_at=article.published_at,
            )

            self.db.add(article_data)

            # Get DB-generated ID
            self.db.flush()

            try:

                text = f"""
                Title:
                {article.title}

                Summary:
                {summary or ''}

                Content:
                {article.content}
                """

                vector = (
                    self.embedding_service
                    .generate_embedding(text)
                )

                payload = {
                    "article_id": article_data.id,
                    "title": article.title,
                    "source": article.source,
                    "url": article.url,
                }

                self.qdrant_service.upsert_article(
                    article_id=article_data.id,
                    vector=vector,
                    payload=payload,
                )

                # -------------------------
                # Cluster Assignment
                # -------------------------

                search_results = (
                    self.qdrant_service.search(
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
                        == article_data.id
                    ):
                        continue

                    similar_article = (
                        self.db.query(Article)
                        .filter(
                            Article.id ==
                            payload["article_id"]
                        )
                        .first()
                    )

                    similarity_score = result.score

                    break

                cluster_id = (
                    self.cluster_service
                    .assign_cluster(
                        article=article_data,
                        similar_article=similar_article,
                        similarity_score=similarity_score,
                    )
                )

                article_data.cluster_id = cluster_id

            except Exception as e:
                print(
                    f"Embedding / Clustering failed: {e}"
                )

            inserted += 1

        self.db.commit()

        return {
            "fetched": len(articles),
            "inserted": inserted,
            "skipped": skipped,
        }

    def get_articles(
        self,
        page: int = 1,
        limit: int = 20,
        source: str | None = None,
    ):
        offset = (page - 1) * limit

        query = self.db.query(Article)

        if source:
            query = query.filter(
                Article.source == source
            )

        return (
            query
            .order_by(
                Article.published_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_article_by_id(
        self,
        article_id: int,
    ):
        return (
            self.db.query(Article)
            .filter(
                Article.id == article_id
            )
            .first()
        )

    def search_articles(
        self,
        query: str,
        page: int = 1,
        limit: int = 20,
    ):
        offset = (page - 1) * limit

        return (
            self.db.query(Article)
            .filter(
                Article.title.ilike(
                    f"%{query}%"
                )
            )
            .order_by(
                Article.published_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def semantic_search(
        self,
        query: str,
        limit: int = 5,
    ):
        vector = (
            self.embedding_service
            .generate_embedding(query)
        )

        results = (
            self.qdrant_service
            .search(
                vector=vector,
                limit=limit,
            )
        )

        article_ids = [
            result.payload["article_id"]
            for result in results.points
        ]

        if not article_ids:
            return []

        articles = (
            self.db.query(Article)
            .filter(
                Article.id.in_(article_ids)
            )
            .all()
        )

        article_map = {
            article.id: article
            for article in articles
        }

        return [
            article_map[article_id]
            for article_id in article_ids
            if article_id in article_map
        ]