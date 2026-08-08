from fastapi import APIRouter

from app.schemas.prediction_schema import (
    PredictionRequest,
    PredictionResponse
)

from app.services.prediction_service import (
    waste_prediction
)


router = APIRouter(
    prefix="/prediction",
    tags=["AI Waste Prediction"]
)


@router.post(
    "/",
    response_model=PredictionResponse
)
def predict(data: PredictionRequest):
    return waste_prediction(data)