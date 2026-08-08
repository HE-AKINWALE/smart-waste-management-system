from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.health_schema import (
    HealthMetricResponse
)

from app.services.health_service import (
    collect_system_metrics,
    get_latest_metrics
)

router = APIRouter(
    prefix="/health",
    tags=["System Health"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/scan",
    response_model=HealthMetricResponse
)
def scan_system(
    db: Session = Depends(get_db)
):

    return collect_system_metrics(db)


@router.get(
    "/latest",
    response_model=HealthMetricResponse
)
def latest_health(
    db: Session = Depends(get_db)
):

    return get_latest_metrics(db)