from datetime import date
from pydantic import BaseModel


class CollectionScheduleCreate(BaseModel):
    user_id: int
    bin_id: int


class CollectionScheduleUpdate(BaseModel):
    schedule_status: str


class CollectionScheduleResponse(BaseModel):
    schedule_id: int
    user_id: int
    bin_id: int
    collection_date: date
    priority_level: str
    schedule_status: str

    class Config:
        from_attributes = True