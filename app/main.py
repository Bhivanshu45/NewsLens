from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.articles import router as articles_router
from app.api.v1.clusters import router as cluster_router

from contextlib import asynccontextmanager
from app.workers.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler.start()

    print("Scheduler Started")

    yield

    scheduler.shutdown()

    print("Scheduler Stopped")

    
app = FastAPI(
    title="NewsLens - News Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"message": "Visit for Intelligence News"}


app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    articles_router,
    prefix="/api/v1",
    tags=["Articles"]
)

app.include_router(
    cluster_router,
    prefix="/api/v1",
    tags=["Clusters"]
)