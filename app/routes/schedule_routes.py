from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.schedule_schema import (
    CollectionScheduleCreate,
    CollectionScheduleUpdate,
    CollectionScheduleResponse,
)

from app.services.schedule_service import (
    create_schedule,
    get_all_schedules,
    get_schedule,
    update_schedule,
    delete_schedule,
    generate_automatic_schedules,
)

router = APIRouter(
    prefix="/schedule",
    tags=["Collection Schedule"]
)


# =========================================================
# AUTOMATIC SCHEDULE GENERATION
# =========================================================

@router.post(
    "/generate",
    response_model=list[CollectionScheduleResponse]
)
def generate_schedule(
    user_id: int,
    db: Session = Depends(get_db)
):

    return generate_automatic_schedules(
        user_id,
        db
    )


# =========================================================
# CREATE SCHEDULE
# =========================================================

@router.post(
    "/",
    response_model=CollectionScheduleResponse
)
def add_schedule(
    schedule: CollectionScheduleCreate,
    db: Session = Depends(get_db)
):

    return create_schedule(
        schedule,
        db
    )


# =========================================================
# GET ALL SCHEDULES
# =========================================================

@router.get(
    "/",
    response_model=list[CollectionScheduleResponse]
)
def all_schedules(
    db: Session = Depends(get_db)
):

    return get_all_schedules(db)


# =========================================================
# GET SINGLE SCHEDULE
# =========================================================

@router.get(
    "/{schedule_id}",
    response_model=CollectionScheduleResponse
)
def view_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    return get_schedule(
        schedule_id,
        db
    )


# =========================================================
# UPDATE SCHEDULE
# =========================================================

@router.put(
    "/{schedule_id}",
    response_model=CollectionScheduleResponse
)
def edit_schedule(
    schedule_id: int,
    schedule: CollectionScheduleUpdate,
    db: Session = Depends(get_db)
):

    return update_schedule(
        schedule_id,
        schedule,
        db
    )


# =========================================================
# DELETE SCHEDULE
# =========================================================

@router.delete(
    "/{schedule_id}"
)
def remove_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    return delete_schedule(
        schedule_id,
        db
    )