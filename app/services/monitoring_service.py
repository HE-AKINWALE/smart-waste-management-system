from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord
from app.models.notification import Notification


def monitoring_dashboard(db: Session):

    total_bins = db.query(WasteBin).count()

    active_bins = db.query(WasteBin).filter(
        WasteBin.bin_status != "Inactive"
    ).count()

    critical_bins = db.query(WasteBin).filter(
        WasteBin.fill_level >= 80
    ).count()

    pending_collections = db.query(CollectionSchedule).filter(
        CollectionSchedule.schedule_status == "Pending"
    ).count()

    completed_collections = db.query(CollectionRecord).count()

    unread_notifications = db.query(Notification).filter(
        Notification.status == "Unread"
    ).count()

    return {
        "system_status": "Online",

        "total_bins": total_bins,

        "active_bins": active_bins,

        "critical_bins": critical_bins,

        "pending_collections": pending_collections,

        "completed_collections": completed_collections,

        "unread_notifications": unread_notifications,

        "server_health": "Healthy"
    }