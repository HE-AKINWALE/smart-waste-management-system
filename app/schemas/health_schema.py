from datetime import datetime
from pydantic import BaseModel


class HealthMetricResponse(BaseModel):

    metric_id: int

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    database_status: str

    api_response_time: float

    created_at: datetime

    model_config = {
        "from_attributes": True
    }