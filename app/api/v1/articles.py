from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.news.news_service import NewsService
from app.services.news.schemas import ArticleResponse


router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


@router.get(
    "",
    response_model=list[ArticleResponse]
)
def get_articles(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    source: str | None = None,
    db: Session = Depends(get_db),
):
    service = NewsService(db)

    return service.get_articles(
        page=page,
        limit=limit,
        source=source,
    )


@router.get(
    "/search",
    response_model=list[ArticleResponse]
)
def search_articles(
    q: str,
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    service = NewsService(db)

    return service.search_articles(
        query=q,
        page=page,
        limit=limit,
    )


@router.get(
    "/semantic-search",
    response_model=list[ArticleResponse]
)
def semantic_search(
    q: str,
    limit: int = Query(
        default=5,
        ge=1,
        le=20,
    ),
    db: Session = Depends(get_db),
):
    service = NewsService(db)

    return service.semantic_search(
        query=q,
        limit=limit,
    )


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    service = NewsService(db)

    article = service.get_article_by_id(
        article_id
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article