from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.notification import Notification


def get_user_notifications(
    user_id: int,
    db: Session
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id
        )
        .order_by(
            Notification.date_created.desc()
        )
        .all()
    )

    return notifications


def get_unread_notification_count(
    user_id: int,
    db: Session
):
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.status == "Unread"
        )
        .count()
    )

    return count


def mark_notification_as_read(
    notification_id: int,
    user_id: int,
    db: Session
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.notification_id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    notification.status = "Read"

    db.commit()
    db.refresh(notification)

    return notification