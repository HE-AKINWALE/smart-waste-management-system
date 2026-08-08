from sqlalchemy.orm import Session

from app.models.user import User
from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord


def executive_dashboard(db: Session):

    total_users = db.query(User).count()

    total_bins = db.query(WasteBin).count()

    full_bins = db.query(WasteBin).filter(
        WasteBin.fill_level >= 80
    ).count()

    pending = db.query(CollectionSchedule).filter(
        CollectionSchedule.schedule_status == "Pending"
    ).count()

    completed = db.query(CollectionRecord).count()

    efficiency = 0

    if pending + completed > 0:
        efficiency = round(
            (completed / (pending + completed)) * 100,
            2
        )

    if efficiency >= 90:
        system_health = "Excellent"

    elif efficiency >= 70:
        system_health = "Good"

    elif efficiency >= 50:
        system_health = "Average"

    else:
        system_health = "Poor"

    return {
        "total_users": total_users,
        "total_bins": total_bins,
        "bins_requiring_collection": full_bins,
        "pending_collections": pending,
        "completed_collections": completed,
        "collection_efficiency": efficiency,
        "system_health": system_health
    }