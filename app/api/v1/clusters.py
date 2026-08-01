from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.api.dependencies import get_cluster_service
from app.services.clustering.cluster_service import ClusterService

from app.services.clustering.schemas import (
    ClusterDetailResponse,
    ClusterResponse,
)

router = APIRouter(
    prefix="/clusters",
    tags=["Clusters"]
)


@router.get(
    "",
    response_model=list[ClusterResponse]
)
def get_clusters(
    service: ClusterService = Depends(get_cluster_service)
):
    return service.list_clusters()


@router.get(
    "/{cluster_id}",
    response_model=ClusterDetailResponse
)
def get_cluster(
    cluster_id: int,
    service: ClusterService = Depends(get_cluster_service)
):
    cluster = service.get_cluster_by_id(
        cluster_id
    )

    if not cluster:
        raise HTTPException(
            status_code=404,
            detail="Cluster not found"
        )

    return cluster