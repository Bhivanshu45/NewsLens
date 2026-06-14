# ingest new articles every 15 minutes

from apscheduler.schedulers.background import BackgroundScheduler

from app.db.session import SessionLocal
from app.services.news.news_service import NewsService


def ingest_new_jobs():
    db = SessionLocal()

    try:
        service = NewsService(db)

        result = service.ingest_articles()

        print(
            f"[Scheduler] "
            f"Fetched={result['fetched']} "
            f"Inserted={result['inserted']} "
            f"Skipped={result['skipped']}"
        )
    
    except Exception as e:
        print(f"[Scheduler] Error during ingestion: {e}")
    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    ingest_new_jobs,
    trigger="interval",
    minutes=15,
    id="news_ingestion",
    replace_existing=True,
)