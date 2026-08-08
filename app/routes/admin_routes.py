from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.admin_schema import SystemSummary
from app.services.admin_service import system_summary


router = APIRouter(
    prefix="/admin",
    tags=["Admin Control Center"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/summary",
    response_model=SystemSummary
)
def admin_dashboard(
    db: Session = Depends(get_db)
):
    return system_summary(db)