from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.db.models.cluster import Cluster

from app.services.clustering.cluster_service import (
    ClusterService
)

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
    db: Session = Depends(get_db)
):
    return (
        db.query(Cluster)
        .order_by(
            Cluster.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{cluster_id}",
    response_model=ClusterDetailResponse
)
def get_cluster(
    cluster_id: int,
    db: Session = Depends(get_db)
):
    service = ClusterService(db)

    cluster = service.get_cluster_by_id(
        cluster_id
    )

    if not cluster:
        raise HTTPException(
            status_code=404,
            detail="Cluster not found"
        )

    return cluster