from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.ai_report_schema import AIReportResponse

from app.services.ai_report_service import generate_ai_report

router = APIRouter(
    prefix="/ai-report",
    tags=["AI Report Generator"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=AIReportResponse
)
def ai_report(
    db: Session = Depends(get_db)
):
    return generate_ai_report(db)