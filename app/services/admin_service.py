from sqlalchemy.orm import Session

from app.models.user import User
from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord
from app.models.notification import Notification


def system_summary(db: Session):

    users = db.query(User).count()

    bins = db.query(WasteBin).count()

    schedules = db.query(CollectionSchedule).count()

    completed = db.query(CollectionRecord).count()

    notifications = db.query(Notification).count()

    return {
        "total_users": users,
        "total_bins": bins,
        "total_schedules": schedules,
        "total_completed_collections": completed,
        "total_notifications": notifications
    }