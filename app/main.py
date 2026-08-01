from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.articles import router as articles_router
from app.api.v1.clusters import router as cluster_router
from app.api.v1.health import router as health_router
from app.api.v1.news import router as news_router
from app.core.constants import API_PREFIX
from app.core.logger import logger
from app.workers.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler.start()

    logger.info("Scheduler started")

    yield

    scheduler.shutdown()

    logger.info("Scheduler stopped")

    
app = FastAPI(
    title="NewsLens - AI News Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"message": "Visit for Intelligence News"}


app.include_router(
    health_router,
    prefix=API_PREFIX,
    tags=["Health"]
)

app.include_router(
    articles_router,
    prefix=API_PREFIX,
    tags=["Articles"]
)

app.include_router(
    cluster_router,
    prefix=API_PREFIX,
    tags=["Clusters"]
)

app.include_router(news_router)


main = app