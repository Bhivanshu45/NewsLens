from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.db.models.cluster import Cluster

router = APIRouter(
    prefix="/clusters",
    tags=["Clusters"]
)


@router.get("")
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