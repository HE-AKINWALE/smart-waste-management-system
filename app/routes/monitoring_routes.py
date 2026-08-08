from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.monitoring_service import monitoring_dashboard

router = APIRouter(
    prefix="/monitoring",
    tags=["Real-Time Monitoring"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def live_dashboard(
    db: Session = Depends(get_db)
):
    return monitoring_dashboard(db)