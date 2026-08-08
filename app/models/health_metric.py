from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.database import Base


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    metric_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    cpu_usage = Column(Float)

    memory_usage = Column(Float)

    disk_usage = Column(Float)

    database_status = Column(
        String(30),
        default="Healthy"
    )

    api_response_time = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )