from pydantic import BaseModel


class RouteResponse(BaseModel):
    order: int
    bin_id: int
    location: str
    fill_level: int
    priority: str