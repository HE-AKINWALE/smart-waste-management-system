from datetime import datetime

from pydantic import BaseModel, ConfigDict

from pydantic import BaseModel


class UnreadNotificationCountResponse(BaseModel):
    unread_count: int


class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str


class NotificationResponse(NotificationBase):
    notification_id: int
    user_id: int
    status: str
    date_created: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationReadResponse(BaseModel):
    notification_id: int
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )