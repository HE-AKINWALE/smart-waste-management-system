from pydantic import BaseModel


class PredictionRequest(BaseModel):
    capacity: float
    fill_level: float
    previous_fill: float
    days_since_collection: int


class PredictionResponse(BaseModel):
    predicted_fill: float
    risk_level: str
    recommended_action: str