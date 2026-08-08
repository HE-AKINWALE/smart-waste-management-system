from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.ml_schema import PredictionResponse

from app.services.ml_service import predict_future_fill

router = APIRouter(

    prefix="/ml",

    tags=["Machine Learning"]

)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


@router.get(

    "/predict/{bin_id}",

    response_model=PredictionResponse

)

def predict(

    bin_id: int,

    db: Session = Depends(get_db)

):

    return predict_future_fill(bin_id, db)