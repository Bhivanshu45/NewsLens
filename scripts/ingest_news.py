from app.db.session import SessionLocal
from app.services.news.news_service import NewsService


db = SessionLocal()

try:
    service = NewsService()

    result = service.ingest_articles(db)

    print(result)

finally:
    db.close()