from sqlalchemy.orm import Session

from app.core.logger import logger
from app.services.news.ingestion_pipeline import NewsIngestionPipeline
from app.services.news.rss_service import RSSService


class NewsService:
    def __init__(
        self,
        db: Session,
        rss_service: RSSService,
        pipeline: NewsIngestionPipeline,
    ):
        self.db = db
        self.rss_service = rss_service
        self.pipeline = pipeline

    def ingest_articles(self):
        articles = self.rss_service.fetch_and_parse_feeds()

        inserted = 0
        skipped = 0

        for article in articles:
            processed = self.pipeline.process_article(article)

            if processed:
                try:
                    self.db.commit()
                    inserted += 1
                except Exception:
                    self.db.rollback()
                    skipped += 1
                    logger.exception(
                        "Failed to commit ingested article: %s",
                        article.url,
                    )
            else:
                self.db.rollback()
                skipped += 1
                logger.info("Skipped article: %s", article.url)

        return {
            "fetched": len(articles),
            "inserted": inserted,
            "skipped": skipped,
        }
