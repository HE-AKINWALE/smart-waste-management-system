from pydantic import BaseModel
from datetime import date


class CollectionRecordCreate(BaseModel):
    schedule_id: int
    completion_date: date
    collection_status: str
    remarks: str | None = None


class CollectionRecordResponse(BaseModel):
    record_id: int
    schedule_id: int
    completion_date: date
    collection_status: str
    remarks: str | None = None

    model_config = {
        "from_attributes": True
    }