from apscheduler.schedulers.background import BackgroundScheduler

from app.core.constants import RSS_FETCH_INTERVAL_MINUTES
from app.core.logger import logger
from app.core.providers import get_news_service
from app.db.session import SessionLocal


def ingest_new_jobs():
    db = SessionLocal()

    try:
        service = get_news_service(db)

        result = service.ingest_articles()

        logger.info(
            "Scheduler ingestion completed: fetched=%s inserted=%s skipped=%s",
            result["fetched"],
            result["inserted"],
            result["skipped"],
        )
    
    except Exception:
        logger.exception("Scheduler ingestion failed")
    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    ingest_new_jobs,
    trigger="interval",
    minutes=RSS_FETCH_INTERVAL_MINUTES,
    id="news_ingestion",
    replace_existing=True,
)