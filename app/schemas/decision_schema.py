from pydantic import BaseModel


class DecisionResponse(BaseModel):
    decision_id: int
    bin_id: int
    decision_type: str
    priority: str
    recommendation: str
    reason: str
    status: str