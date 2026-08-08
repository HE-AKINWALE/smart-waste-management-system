from sqlalchemy.orm import Session

from app.models.user import User
from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord


def generate_ai_report(db: Session):

    total_users = db.query(User).count()

    total_bins = db.query(WasteBin).count()

    full_bins = db.query(
        WasteBin
    ).filter(
        WasteBin.fill_level >= 80
    ).count()

    pending = db.query(
        CollectionSchedule
    ).filter(
        CollectionSchedule.schedule_status == "Pending"
    ).count()

    completed = db.query(
        CollectionRecord
    ).count()

    efficiency = 0

    if pending + completed > 0:
        efficiency = round(
            (completed / (pending + completed)) * 100,
            2
        )

    recommendations = []

    if full_bins > 0:
        recommendations.append(
            f"{full_bins} waste bins require immediate attention."
        )

    if pending > 10:
        recommendations.append(
            "Deploy additional collection vehicles."
        )

    if efficiency < 70:
        recommendations.append(
            "Collection efficiency is below target."
        )

    if efficiency >= 90:
        recommendations.append(
            "Current waste collection performance is excellent."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "System is operating normally."
        )

    return {
        "summary": {
            "total_users": total_users,
            "total_bins": total_bins,
            "full_bins": full_bins,
            "pending_collections": pending,
            "completed_collections": completed,
            "collection_efficiency": efficiency
        },
        "recommendations": recommendations
    }