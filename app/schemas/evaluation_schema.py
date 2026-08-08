from pydantic import BaseModel


class EvaluationResponse(BaseModel):
    prediction_accuracy: float
    optimization_score: float
    decision_efficiency: float
    overall_system_score: float