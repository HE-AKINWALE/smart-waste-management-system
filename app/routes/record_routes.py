from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.record_schema import (
    CollectionRecordCreate,
    CollectionRecordResponse
)

from app.services.record_service import (
    create_record,
    get_all_records,
    get_record
)

router = APIRouter(
    prefix="/records",
    tags=["Collection Records"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CollectionRecordResponse)
def add_record(
    record: CollectionRecordCreate,
    db: Session = Depends(get_db)
):
    return create_record(record, db)


@router.get("/", response_model=list[CollectionRecordResponse])
def all_records(
    db: Session = Depends(get_db)
):
    return get_all_records(db)


@router.get("/{record_id}", response_model=CollectionRecordResponse)
def single_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = get_record(record_id, db)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Collection record not found"
        )

    return record