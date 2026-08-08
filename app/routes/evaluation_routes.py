from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.evaluation_schema import (
    EvaluationResponse
)

from app.services.evaluation_service import (
    evaluate_system
)

router = APIRouter(
    prefix="/evaluation",
    tags=["AI Performance Evaluation"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=EvaluationResponse
)
def system_evaluation(
    db: Session = Depends(get_db)
):

    return evaluate_system(db)