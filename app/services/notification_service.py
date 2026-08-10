from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.notification import Notification


# =========================================================
# CREATE NOTIFICATION
# =========================================================

def create_notification(
    user_id: int,
    title: str,
    message: str,
    notification_type: str,
    db: Session
):
    """
    Create a new unread notification for a user.
    """

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        status="Unread",
        date_created=datetime.now(),
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


# =========================================================
# GET USER NOTIFICATIONS
# =========================================================

def get_user_notifications(
    user_id: int,
    db: Session
):
    """
    Return all notifications belonging to a user,
    newest first.
    """

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


# =========================================================
# GET UNREAD NOTIFICATION COUNT
# =========================================================

def get_unread_notification_count(
    user_id: int,
    db: Session
):
    """
    Return the number of unread notifications
    belonging to a user.
    """

    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.status == "Unread"
        )
        .count()
    )

    return count


# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================

def mark_notification_as_read(
    notification_id: int,
    user_id: int,
    db: Session
):
    """
    Mark a specific notification as read.

    The notification must belong to the authenticated user.
    """

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