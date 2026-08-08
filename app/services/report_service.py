from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord
from app.models.notification import Notification
from datetime import date
from sqlalchemy import and_
from datetime import timedelta
from sqlalchemy import extract

def dashboard_report(db: Session):

    total_users = db.query(User).count()

    total_bins = db.query(WasteBin).count()

    active_bins = (
        db.query(WasteBin)
        .filter(WasteBin.bin_status == "Active")
        .count()
    )

    full_bins = (
        db.query(WasteBin)
        .filter(WasteBin.fill_level >= 80)
        .count()
    )

    pending_schedules = (
        db.query(CollectionSchedule)
        .filter(CollectionSchedule.schedule_status == "Pending")
        .count()
    )

    completed_collections = (
        db.query(CollectionSchedule)
        .filter(CollectionSchedule.schedule_status == "Completed")
        .count()
    )

    total_notifications = db.query(Notification).count()

    if pending_schedules + completed_collections == 0:
        efficiency = 0
    else:
        efficiency = round(
            completed_collections /
            (completed_collections + pending_schedules)
            * 100,
            2
        )

    return {
        "total_users": total_users,
        "total_bins": total_bins,
        "active_bins": active_bins,
        "full_bins": full_bins,
        "pending_schedules": pending_schedules,
        "completed_collections": completed_collections,
        "total_notifications": total_notifications,
        "collection_efficiency": efficiency
    }

def bin_status_report(db: Session):

    active = (
        db.query(WasteBin)
        .filter(WasteBin.bin_status == "Active")
        .count()
    )

    inactive = (
        db.query(WasteBin)
        .filter(WasteBin.bin_status == "Inactive")
        .count()
    )

    full = (
        db.query(WasteBin)
        .filter(WasteBin.fill_level >= 80)
        .count()
    )

    return {
        "active_bins": active,
        "inactive_bins": inactive,
        "full_bins": full
    }

def fill_level_distribution(db: Session):

    low = db.query(WasteBin).filter(
        WasteBin.fill_level < 25
    ).count()

    medium = db.query(WasteBin).filter(
        and_(
            WasteBin.fill_level >= 25,
            WasteBin.fill_level < 50
        )
    ).count()

    high = db.query(WasteBin).filter(
        and_(
            WasteBin.fill_level >= 50,
            WasteBin.fill_level < 80
        )
    ).count()

    critical = db.query(WasteBin).filter(
        WasteBin.fill_level >= 80
    ).count()

    return {
        "low": low,
        "medium": medium,
        "high": high,
        "critical": critical
    }

def critical_bins(db: Session):

    return (
        db.query(WasteBin)
        .filter(WasteBin.fill_level >= 80)
        .all()
    )

def weekly_schedule(db: Session):

    today = date.today()

    end_date = today + timedelta(days=7)

    return (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.collection_date >= today,
            CollectionSchedule.collection_date <= end_date
        )
        .all()
    )

def monthly_collections(db: Session):

    today = date.today()

    return (
        db.query(CollectionRecord)
        .filter(
            extract("month", CollectionRecord.completion_date) == today.month,
            extract("year", CollectionRecord.completion_date) == today.year
        )
        .all()
    )

def system_health(db: Session):

    pending = (
        db.query(CollectionSchedule)
        .filter(CollectionSchedule.schedule_status == "Pending")
        .count()
    )

    completed = (
        db.query(CollectionRecord)
        .filter(CollectionRecord.collection_status == "Completed")
        .count()
    )

    notifications = db.query(Notification).count()

    efficiency = 0

    if pending + completed > 0:

        efficiency = round(
            completed /
            (pending + completed) * 100,
            2
        )

    return {
        "collection_efficiency": efficiency,
        "notification_count": notifications,
        "pending_schedules": pending,
        "completed_collections": completed
    }