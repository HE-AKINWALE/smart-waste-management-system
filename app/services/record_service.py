from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.collection_record import CollectionRecord
from app.models.collection_schedule import CollectionSchedule
from app.models.waste_bin import WasteBin

from app.schemas.record_schema import (
    CollectionRecordCreate,
)


# =========================================================
# CREATE COLLECTION RECORD
# =========================================================

def create_record(
    record: CollectionRecordCreate,
    db: Session
):

    schedule = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.schedule_id
            == record.schedule_id
        )
        .first()
    )

    if schedule is None:
        raise HTTPException(
            status_code=404,
            detail="Collection schedule not found."
        )

    # Prevent duplicate records
    existing_record = (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.schedule_id
            == record.schedule_id
        )
        .first()
    )

    if existing_record is not None:
        raise HTTPException(
            status_code=400,
            detail="A collection record already exists for this schedule."
        )

    new_record = CollectionRecord(
        schedule_id=record.schedule_id,
        completion_date=record.completion_date,
        collection_status=record.collection_status,
        remarks=record.remarks
    )

    db.add(new_record)

    # Mark the schedule as completed
    schedule.schedule_status = "Completed"

    # Empty the bin after collection
    waste_bin = (
        db.query(WasteBin)
        .filter(
            WasteBin.bin_id == schedule.bin_id
        )
        .first()
    )

    if waste_bin:
        waste_bin.fill_level = 0
        waste_bin.bin_status = "Empty"

    db.commit()

    db.refresh(new_record)

    return new_record


# =========================================================
# GET ALL RECORDS
# =========================================================

def get_all_records(db: Session):

    return (
        db.query(CollectionRecord)
        .order_by(
            CollectionRecord.record_id.desc()
        )
        .all()
    )


# =========================================================
# GET SINGLE RECORD
# =========================================================

def get_record(
    record_id: int,
    db: Session
):

    return (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.record_id
            == record_id
        )
        .first()
    )