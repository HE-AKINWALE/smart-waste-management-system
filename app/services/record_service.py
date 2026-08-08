from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.collection_record import CollectionRecord
from app.models.collection_schedule import CollectionSchedule
from app.schemas.record_schema import CollectionRecordCreate


def create_record(
    record: CollectionRecordCreate,
    db: Session
):
    # Check that the schedule exists
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

    # Check whether this schedule already has a record
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
    db.commit()
    db.refresh(new_record)

    return new_record


def get_all_records(db: Session):
    return (
        db.query(CollectionRecord)
        .order_by(CollectionRecord.record_id.desc())
        .all()
    )


def get_record(
    record_id: int,
    db: Session
):
    return (
        db.query(CollectionRecord)
        .filter(
            CollectionRecord.record_id == record_id
        )
        .first()
    )