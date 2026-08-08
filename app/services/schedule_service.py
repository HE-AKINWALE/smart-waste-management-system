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
)


def create_schedule(data: CollectionScheduleCreate, db: Session):

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

    priority = calculate_priority(waste_bin.fill_level)

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


def get_all_schedules(db: Session):
    return db.query(CollectionSchedule).all()


def get_schedule(schedule_id: int, db: Session):
    return (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.schedule_id == schedule_id
        )
        .first()
    )


def update_schedule(
    schedule_id: int,
    data: CollectionScheduleUpdate,
    db: Session,
):

    schedule = get_schedule(schedule_id, db)

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found."
        )

    waste_bin = (
        db.query(WasteBin)
        .filter(WasteBin.bin_id == schedule.bin_id)
        .first()
    )

    if waste_bin is None:
        raise HTTPException(
            status_code=404,
            detail="Waste bin not found."
        )

    schedule.collection_date = recommend_collection_date(
        waste_bin.fill_level
    )

    schedule.priority_level = calculate_priority(
        waste_bin.fill_level
    )

    if data.schedule_status is not None:
        schedule.schedule_status = data.schedule_status

    db.commit()
    db.refresh(schedule)

    return schedule


def delete_schedule(
    schedule_id: int,
    db: Session,
):

    schedule = get_schedule(schedule_id, db)

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found."
        )

    db.delete(schedule)
    db.commit()

    return {
        "message": "Schedule deleted successfully."
    }