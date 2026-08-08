from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.dashboard_schema import DashboardResponse

from app.services.dashboard_service import executive_dashboard


router = APIRouter(
    prefix="/executive-dashboard",
    tags=["Executive Dashboard"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=DashboardResponse
)
def dashboard(
    db: Session = Depends(get_db)
):
    return executive_dashboard(db)