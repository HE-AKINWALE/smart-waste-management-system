from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.collection_processor import process_due_collections

from app.schemas.record_schema import (
    CollectionRecordCreate,
    CollectionRecordResponse,
)

from app.services.record_service import (
    create_record,
    get_all_records,
    get_record,
)

router = APIRouter(
    prefix="/records",
    tags=["Collection Records"]
)


# =========================================================
# CREATE COLLECTION RECORD
# =========================================================

@router.post(
    "/",
    response_model=CollectionRecordResponse
)
def add_record(
    record: CollectionRecordCreate,
    db: Session = Depends(get_db)
):
    return create_record(record, db)


# =========================================================
# GET ALL COLLECTION RECORDS
# =========================================================

@router.get(
    "/",
    response_model=list[CollectionRecordResponse]
)
def all_records(
    db: Session = Depends(get_db)
):
    return get_all_records(db)


# =========================================================
# AUTOMATIC COLLECTION PROCESSING
# =========================================================

@router.post("/process-due")
def process_due_collections_route(
    db: Session = Depends(get_db)
):

    processed = process_due_collections(db)

    return {
        "message": "Due collections processed successfully.",
        "processed_count": len(processed),
        "schedule_ids": processed
    }


# =========================================================
# GET SINGLE COLLECTION RECORD
# =========================================================

@router.get(
    "/{record_id}",
    response_model=CollectionRecordResponse
)
def single_record(
    record_id: int,
    db: Session = Depends(get_db)
):

    record = get_record(
        record_id,
        db
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Collection record not found."
        )

    return record