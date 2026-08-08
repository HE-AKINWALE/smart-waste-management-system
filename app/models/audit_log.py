from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(Integer)

    activity = Column(String(255))

    module = Column(String(100))

    ip_address = Column(String(100))

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )