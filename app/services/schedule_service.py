from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.collection_schedule import CollectionSchedule
from app.models.waste_bin import WasteBin

from app.schemas.schedule_schema import (
    CollectionScheduleCreate,
    CollectionScheduleUpdate,
)

from app.services.intelligent_scheduler import (
    calculate_priority,
    recommend_collection_date,
    requires_collection,
)


# =========================================================
# MANUAL / ADMIN OVERRIDE
# =========================================================

def create_schedule(
    data: CollectionScheduleCreate,
    db: Session
):

    waste_bin = (
        db.query(WasteBin)
        .filter(WasteBin.bin_id == data.bin_id)
        .first()
    )

    if waste_bin is None:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found."
        )

    priority = calculate_priority(
        waste_bin.fill_level
    )

    recommended_date = recommend_collection_date(
        waste_bin.fill_level
    )

    schedule = CollectionSchedule(
        user_id=data.user_id,
        bin_id=data.bin_id,
        collection_date=recommended_date,
        priority_level=priority,
        schedule_status="Pending",
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


# =========================================================
# AUTOMATIC SCHEDULE GENERATION
# =========================================================

def generate_automatic_schedules(
    user_id: int,
    db: Session
):
    """
    Automatically generate collection schedules
    based on the current fill level of waste bins.
    """

    waste_bins = (
        db.query(WasteBin)
        .order_by(WasteBin.fill_level.desc())
        .all()
    )

    generated_schedules = []

    for waste_bin in waste_bins:

        # Skip bins that don't currently require collection
        if not requires_collection(
            waste_bin.fill_level
        ):
            continue

        # Check whether this bin already has a
        # pending schedule.
        existing_schedule = (
            db.query(CollectionSchedule)
            .filter(
                CollectionSchedule.bin_id
                == waste_bin.bin_id,

                CollectionSchedule.schedule_status
                == "Pending"
            )
            .first()
        )

        # Don't create duplicate schedules
        if existing_schedule:
            continue

        priority = calculate_priority(
            waste_bin.fill_level
        )

        collection_date = (
            recommend_collection_date(
                waste_bin.fill_level
            )
        )

        schedule = CollectionSchedule(
            user_id=user_id,
            bin_id=waste_bin.bin_id,
            collection_date=collection_date,
            priority_level=priority,
            schedule_status="Pending",
        )

        db.add(schedule)

        generated_schedules.append(
            schedule
        )

    db.commit()

    # Refresh generated records
    for schedule in generated_schedules:
        db.refresh(schedule)

    return generated_schedules


# =========================================================
# GET ALL
# =========================================================

def get_all_schedules(
    db: Session
):

    return (
        db.query(CollectionSchedule)
        .order_by(
            CollectionSchedule.collection_date.asc()
        )
        .all()
    )


# =========================================================
# GET SINGLE
# =========================================================

def get_schedule(
    schedule_id: int,
    db: Session
):

    schedule = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.schedule_id
            == schedule_id
        )
        .first()
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found."
        )

    return schedule


# =========================================================
# UPDATE
# =========================================================

def update_schedule(
    schedule_id: int,
    data: CollectionScheduleUpdate,
    db: Session,
):

    schedule = get_schedule(
        schedule_id,
        db
    )

    waste_bin = (
        db.query(WasteBin)
        .filter(
            WasteBin.bin_id
            == schedule.bin_id
        )
        .first()
    )

    if waste_bin is None:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found."
        )

    # Recalculate intelligently
    schedule.collection_date = (
        recommend_collection_date(
            waste_bin.fill_level
        )
    )

    schedule.priority_level = (
        calculate_priority(
            waste_bin.fill_level
        )
    )

    # Allow administrator to override status
    if data.schedule_status is not None:
        schedule.schedule_status = (
            data.schedule_status
        )

    db.commit()
    db.refresh(schedule)

    return schedule


# =========================================================
# DELETE
# =========================================================

def delete_schedule(
    schedule_id: int,
    db: Session,
):

    schedule = get_schedule(
        schedule_id,
        db
    )

    db.delete(schedule)
    db.commit()

    return {
        "message":
        "Schedule deleted successfully."
    }