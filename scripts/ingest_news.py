from app.core.logger import logger
from app.core.providers import get_news_service
from app.db.session import SessionLocal


db = SessionLocal()

try:
    service = get_news_service(db)

    result = service.ingest_articles()

    logger.info("Ingestion result: %s", result)

finally:
    db.close()