from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord


def evaluate_system(db: Session):

    total_bins = db.query(WasteBin).count()

    full_bins = db.query(WasteBin).filter(
        WasteBin.fill_level >= 80
    ).count()

    total_schedules = db.query(CollectionSchedule).count()

    completed = db.query(CollectionRecord).count()

    if total_bins == 0:
        prediction_accuracy = 100
    else:
        prediction_accuracy = round(
            ((total_bins - full_bins) / total_bins) * 100,
            2
        )

    if total_schedules == 0:
        optimization_score = 100
    else:
        optimization_score = round(
            (completed / total_schedules) * 100,
            2
        )

    decision_efficiency = round(
        (prediction_accuracy + optimization_score) / 2,
        2
    )

    overall_score = round(
        (
            prediction_accuracy +
            optimization_score +
            decision_efficiency
        ) / 3,
        2
    )

    return {
        "prediction_accuracy": prediction_accuracy,
        "optimization_score": optimization_score,
        "decision_efficiency": decision_efficiency,
        "overall_system_score": overall_score
    }