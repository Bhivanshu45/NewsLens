from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from app.api.dependencies import get_article_search_service
from app.core.constants import DEFAULT_ARTICLE_LIMIT, QDRANT_SEARCH_LIMIT
from app.services.search.article_search_service import ArticleSearchService
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
        default=DEFAULT_ARTICLE_LIMIT,
        ge=1,
        le=100,
    ),
    source: str | None = None,
    service: ArticleSearchService = Depends(get_article_search_service),
):
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
        default=DEFAULT_ARTICLE_LIMIT,
        ge=1,
        le=100,
    ),
    service: ArticleSearchService = Depends(get_article_search_service),
):
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
        default=QDRANT_SEARCH_LIMIT,
        ge=1,
        le=20,
    ),
    service: ArticleSearchService = Depends(get_article_search_service),
):
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
    service: ArticleSearchService = Depends(get_article_search_service),
):
    article = service.get_article_by_id(
        article_id
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article