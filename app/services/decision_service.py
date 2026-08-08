from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule


def generate_decisions(db: Session):

    decisions = []

    bins = db.query(WasteBin).all()

    decision_id = 1

    for waste_bin in bins:

        fill_level = waste_bin.fill_level or 0

        if fill_level >= 90:

            decisions.append({
                "decision_id": decision_id,
                "bin_id": waste_bin.bin_id,
                "decision_type": "Immediate Collection",
                "priority": "Critical",
                "recommendation": (
                    f"Dispatch collection truck immediately to "
                    f"{waste_bin.bin_location}."
                ),
                "reason": (
                    f"Bin fill level has reached {fill_level}%, "
                    "which indicates a critical waste level."
                ),
                "status": "Pending"
            })

            decision_id += 1

        elif fill_level >= 75:

            decisions.append({
                "decision_id": decision_id,
                "bin_id": waste_bin.bin_id,
                "decision_type": "Collection Scheduling",
                "priority": "High",
                "recommendation": (
                    f"Schedule waste collection today for "
                    f"{waste_bin.bin_location}."
                ),
                "reason": (
                    f"Bin fill level is currently {fill_level}%, "
                    "which is approaching full capacity."
                ),
                "status": "Pending"
            })

            decision_id += 1

        elif fill_level >= 50:

            decisions.append({
                "decision_id": decision_id,
                "bin_id": waste_bin.bin_id,
                "decision_type": "Waste Level Monitoring",
                "priority": "Medium",
                "recommendation": (
                    f"Monitor waste level at "
                    f"{waste_bin.bin_location}."
                ),
                "reason": (
                    f"Bin fill level is currently {fill_level}%. "
                    "Collection is not yet urgent."
                ),
                "status": "Monitoring"
            })

            decision_id += 1

    pending = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.schedule_status == "Pending"
        )
        .count()
    )

    if pending > 10:

        decisions.append({
            "decision_id": decision_id,
            "bin_id": 0,
            "decision_type": "Collection Capacity",
            "priority": "High",
            "recommendation": (
                "Deploy additional collection vehicles "
                "to reduce the pending collection queue."
            ),
            "reason": (
                f"There are currently {pending} pending "
                "collection schedules."
            ),
            "status": "Pending"
        })

        decision_id += 1

    if not decisions:

        decisions.append({
            "decision_id": decision_id,
            "bin_id": 0,
            "decision_type": "System Monitoring",
            "priority": "Normal",
            "recommendation": (
                "Waste management system is operating efficiently."
            ),
            "reason": (
                "No waste bins currently require urgent "
                "collection or monitoring."
            ),
            "status": "Stable"
        })

    return decisions