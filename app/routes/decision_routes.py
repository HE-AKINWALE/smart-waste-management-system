from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.decision_schema import DecisionResponse
from app.services.decision_service import generate_decisions


router = APIRouter(
    prefix="/decision",
    tags=["AI Decision Engine"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[DecisionResponse]
)
def decision_dashboard(
    db: Session = Depends(get_db)
):
    return generate_decisions(db)