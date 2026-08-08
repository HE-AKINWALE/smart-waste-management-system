from pydantic import BaseModel


class OptimizedRouteResponse(BaseModel):
    order: int
    bin_id: int
    location: str
    fill_level: int
    priority: str

    estimated_waste: float
    optimization_score: float
    recommended_action: str

    class Config:
        from_attributes = True