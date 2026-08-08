from pydantic import BaseModel
from datetime import datetime


class AuditLogCreate(BaseModel):
    user_id: int
    activity: str
    module: str
    ip_address: str


class AuditLogResponse(BaseModel):
    audit_id: int
    user_id: int
    activity: str
    module: str
    ip_address: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }