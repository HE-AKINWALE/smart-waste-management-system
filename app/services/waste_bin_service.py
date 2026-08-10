from sqlalchemy.orm import Session

from app.models.waste_bin import WasteBin
from app.models.collection_schedule import CollectionSchedule

from app.schemas.waste_bin_schema import (
    WasteBinCreate,
    WasteBinUpdate,
)

from app.services.intelligent_scheduler import (
    calculate_priority,
    recommend_collection_date,
    requires_collection,
)


# =========================================================
# CALCULATE BIN STATUS
# =========================================================

def calculate_status(fill_level: int):

    if fill_level == 0:
        return "Empty"

    elif fill_level <= 49:
        return "Low"

    elif fill_level <= 79:
        return "Medium"

    elif fill_level <= 99:
        return "High"

    else:
        return "Full"


# =========================================================
# CREATE WASTE BIN
# =========================================================

def create_bin(
    bin_data: WasteBinCreate,
    db: Session,
    user_id: int,
):

    waste_bin = WasteBin(
        user_id=user_id,

        bin_location=bin_data.bin_location,

        capacity=bin_data.capacity,

        fill_level=bin_data.fill_level,

        bin_status=calculate_status(
            bin_data.fill_level
        ),
    )

    db.add(waste_bin)

    # Generate bin ID before creating schedule
    db.flush()

    # =====================================================
    # AUTOMATIC COLLECTION SCHEDULING
    # =====================================================

    if requires_collection(
        waste_bin.fill_level
    ):

        create_automatic_schedule(
            waste_bin=waste_bin,
            user_id=user_id,
            db=db,
        )

    db.commit()

    db.refresh(waste_bin)

    return waste_bin


# =========================================================
# GET ALL BINS
# =========================================================

def get_all_bins(
    db: Session,
    current_user,
):

    # =====================================================
    # ADMIN / WASTE OFFICER
    # =====================================================

    if current_user.role.lower() in {
        "admin",
        "waste officer",
    }:

        return (
            db.query(WasteBin)
            .order_by(
                WasteBin.bin_id.asc()
            )
            .all()
        )

    # =====================================================
    # NORMAL USER
    # =====================================================

    return (
        db.query(WasteBin)
        .filter(
            WasteBin.user_id
            == current_user.user_id
        )
        .order_by(
            WasteBin.bin_id.asc()
        )
        .all()
    )


# =========================================================
# GET SINGLE BIN
# =========================================================

def get_bin(
    bin_id: int,
    db: Session,
    current_user,
):

    query = (
        db.query(WasteBin)
        .filter(
            WasteBin.bin_id == bin_id
        )
    )

    # Admin / Waste Officer can see all bins
    if current_user.role.lower() not in {
        "admin",
        "waste officer",
    }:

        query = query.filter(
            WasteBin.user_id
            == current_user.user_id
        )

    return query.first()


# =========================================================
# UPDATE WASTE BIN
# =========================================================

def update_bin(
    bin_id: int,
    bin_data: WasteBinUpdate,
    db: Session,
    current_user,
):

    waste_bin = get_bin(
        bin_id,
        db,
        current_user,
    )

    if waste_bin is None:
        return None

    # =====================================================
    # UPDATE DETAILS
    # =====================================================

    waste_bin.bin_location = (
        bin_data.bin_location
    )

    waste_bin.capacity = (
        bin_data.capacity
    )

    waste_bin.fill_level = (
        bin_data.fill_level
    )

    # Automatically recalculate status
    waste_bin.bin_status = calculate_status(
        bin_data.fill_level
    )

    # =====================================================
    # AUTOMATIC SCHEDULING
    # =====================================================

    if requires_collection(
        waste_bin.fill_level
    ):

        create_automatic_schedule(
            waste_bin=waste_bin,
            user_id=waste_bin.user_id,
            db=db,
        )

    db.commit()

    db.refresh(waste_bin)

    return waste_bin


# =========================================================
# CREATE AUTOMATIC COLLECTION SCHEDULE
# =========================================================

def create_automatic_schedule(
    waste_bin: WasteBin,
    user_id: int,
    db: Session,
):

    # =====================================================
    # PREVENT DUPLICATE PENDING SCHEDULES
    # =====================================================

    existing_schedule = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.bin_id
            == waste_bin.bin_id,

            CollectionSchedule.schedule_status
            == "Pending",
        )
        .first()
    )

    if existing_schedule:

        return existing_schedule

    # =====================================================
    # CALCULATE INTELLIGENT PRIORITY
    # =====================================================

    priority = calculate_priority(
        waste_bin.fill_level
    )

    # =====================================================
    # RECOMMEND COLLECTION DATE
    # =====================================================

    collection_date = (
        recommend_collection_date(
            waste_bin.fill_level
        )
    )

    # =====================================================
    # CREATE SCHEDULE
    # =====================================================

    schedule = CollectionSchedule(

        user_id=user_id,

        bin_id=waste_bin.bin_id,

        collection_date=collection_date,

        priority_level=priority,

        schedule_status="Pending",
    )

    db.add(schedule)

    return schedule


# =========================================================
# DELETE WASTE BIN
# =========================================================

def delete_bin(
    bin_id: int,
    db: Session,
    current_user,
):
    waste_bin = get_bin(
        bin_id,
        db,
        current_user,
    )

    if waste_bin is None:
        return False

    # Find schedules belonging to this bin
    schedules = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.bin_id == bin_id
        )
        .all()
    )

    # Delete related schedules first
    for schedule in schedules:
        db.delete(schedule)

    # Delete the bin
    db.delete(waste_bin)

    db.commit()

    return True