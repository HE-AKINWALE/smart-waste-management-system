from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.auth_bearer import verify_token

from app.schemas.notification_schema import (
    NotificationResponse,
    UnreadNotificationCountResponse,
)

from app.services.notification_service import (
    get_user_notifications,
    get_unread_notification_count,
    mark_notification_as_read,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "/",
    response_model=list[NotificationResponse]
)
def get_notifications(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user_id = token_data.get("user_id")

    return get_user_notifications(
        int(user_id),
        db
    )


@router.get(
    "/unread-count",
    response_model=UnreadNotificationCountResponse
)
def unread_notification_count(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user_id = token_data.get("user_id")

    count = get_unread_notification_count(
        int(user_id),
        db
    )

    return {
        "unread_count": count
    }


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_as_read(
    notification_id: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    user_id = token_data.get("user_id")

    return mark_notification_as_read(
        notification_id,
        int(user_id),
        db
    )