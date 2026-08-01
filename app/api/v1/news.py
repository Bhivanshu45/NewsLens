from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.api.dependencies import get_news_service
from app.core.logger import logger
from app.services.news.news_service import NewsService


router = APIRouter(
    prefix="/api/v1/news",
    tags=["News"],
)


@router.post(
    "/ingest",
    summary="Trigger News Ingestion",
    description="Manually trigger the complete RSS ingestion pipeline. Development/Admin endpoint.",
)
def ingest_news(
    news_service: NewsService = Depends(get_news_service),
):
    try:
        return news_service.ingest_articles()
    except Exception:
        logger.exception("Manual news ingestion failed")
        raise HTTPException(
            status_code=500,
            detail="News ingestion failed",
        )