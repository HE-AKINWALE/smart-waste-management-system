from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_fill_level: float
    recommendation: str