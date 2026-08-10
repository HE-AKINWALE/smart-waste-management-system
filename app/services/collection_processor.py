from datetime import date

from sqlalchemy.orm import Session

from app.models.collection_schedule import CollectionSchedule
from app.models.collection_record import CollectionRecord
from app.models.waste_bin import WasteBin
from app.models.user import User

from app.services.intelligent_scheduler import (
    calculate_priority,
    recommend_collection_date,
    requires_collection,
)

from app.services.notification_service import create_notification


# =========================================================
# GET SYSTEM USER
# =========================================================

def get_system_user_id(db: Session):
    """
    Find a suitable user account to own automatically
    generated collection schedules.

    Admin users are preferred.
    """

    admin = (
        db.query(User)
        .filter(
            User.role.ilike("admin")
        )
        .first()
    )

    if admin:
        return admin.user_id

    user = (
        db.query(User)
        .order_by(
            User.user_id.asc()
        )
        .first()
    )

    if user:
        return user.user_id

    return None


# =========================================================
# GENERATE AUTOMATIC COLLECTION SCHEDULES
# =========================================================

def generate_automatic_schedules(db: Session):
    """
    Automatically create collection schedules for waste bins
    that require collection.

    A bin requiring collection is automatically scheduled.

    Duplicate pending schedules are prevented.

    A notification is also created for the user who owns
    the waste bin.
    """

    system_user_id = get_system_user_id(db)

    if system_user_id is None:
        print(
            "Automatic scheduler: No user account exists. "
            "Cannot create schedules."
        )
        return []

    # -----------------------------------------------------
    # GET ALL WASTE BINS
    # -----------------------------------------------------

    waste_bins = (
        db.query(WasteBin)
        .order_by(
            WasteBin.fill_level.desc()
        )
        .all()
    )

    generated = []

    # -----------------------------------------------------
    # PROCESS EACH BIN
    # -----------------------------------------------------

    for waste_bin in waste_bins:

        # -------------------------------------------------
        # CHECK WHETHER COLLECTION IS REQUIRED
        # -------------------------------------------------

        if not requires_collection(
            waste_bin.fill_level
        ):
            continue

        # -------------------------------------------------
        # PREVENT DUPLICATE PENDING SCHEDULES
        # -------------------------------------------------

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
            continue

        # -------------------------------------------------
        # CALCULATE INTELLIGENT SCHEDULE
        # -------------------------------------------------

        priority = calculate_priority(
            waste_bin.fill_level
        )

        collection_date = recommend_collection_date(
            waste_bin.fill_level
        )

        # -------------------------------------------------
        # DETERMINE NOTIFICATION USER
        # -------------------------------------------------

        # If the bin belongs to a specific user,
        # notify that user.

        # Otherwise, fall back to the system/admin user.

        notification_user_id = (
            waste_bin.user_id
            if waste_bin.user_id is not None
            else system_user_id
        )

        # -------------------------------------------------
        # CREATE COLLECTION SCHEDULE
        # -------------------------------------------------

        schedule = CollectionSchedule(
            user_id=notification_user_id,
            bin_id=waste_bin.bin_id,
            collection_date=collection_date,
            priority_level=priority,
            schedule_status="Pending",
        )

        db.add(schedule)
        db.flush()

        generated.append(schedule)

        # -------------------------------------------------
        # CREATE NOTIFICATION
        # -------------------------------------------------

        create_notification(
            user_id=notification_user_id,

            title="Collection Scheduled",

            message=(
                f"Waste bin #{waste_bin.bin_id} has reached "
                f"a fill level of {waste_bin.fill_level}%. "
                f"A {priority.lower()} priority collection "
                f"has been scheduled for "
                f"{collection_date.strftime('%Y-%m-%d')}."
            ),

            notification_type="Collection",

            db=db,
        )

    # -----------------------------------------------------
    # SAVE GENERATED SCHEDULES
    # -----------------------------------------------------

    if generated:
        db.commit()

        for schedule in generated:
            db.refresh(schedule)

    return generated


# =========================================================
# PROCESS DUE COLLECTIONS
# =========================================================

def process_due_collections(db: Session):
    """
    Automatically:

    1. Generate schedules for bins requiring collection.
    2. Find schedules whose collection date has arrived.
    3. Create collection records automatically.
    4. Mark schedules as completed.
    5. Empty collected bins automatically.
    6. Create notifications for completed collections.
    """

    # =====================================================
    # STEP 1 — GENERATE AUTOMATIC COLLECTION SCHEDULES
    # =====================================================

    generated_schedules = generate_automatic_schedules(
        db
    )

    if generated_schedules:

        print(
            "Automatically generated schedules:",
            [
                schedule.schedule_id
                for schedule in generated_schedules
            ],
        )

    # =====================================================
    # STEP 2 — FIND DUE SCHEDULES
    # =====================================================

    today = date.today()

    due_schedules = (
        db.query(CollectionSchedule)
        .filter(
            CollectionSchedule.collection_date <= today,

            CollectionSchedule.schedule_status
            == "Pending",
        )
        .all()
    )

    processed = []

    # =====================================================
    # STEP 3 — PROCESS EACH DUE COLLECTION
    # =====================================================

    for schedule in due_schedules:

        # -------------------------------------------------
        # FIND THE BIN
        # -------------------------------------------------

        waste_bin = (
            db.query(WasteBin)
            .filter(
                WasteBin.bin_id
                == schedule.bin_id
            )
            .first()
        )

        # -------------------------------------------------
        # CHECK FOR EXISTING COLLECTION RECORD
        # -------------------------------------------------

        existing_record = (
            db.query(CollectionRecord)
            .filter(
                CollectionRecord.schedule_id
                == schedule.schedule_id
            )
            .first()
        )

        # -------------------------------------------------
        # CREATE COLLECTION RECORD
        # -------------------------------------------------

        if existing_record is None:

            record = CollectionRecord(
                schedule_id=schedule.schedule_id,

                completion_date=today,

                collection_status="Completed",

                remarks=(
                    "Collection automatically processed "
                    "by the Smart Waste Management System."
                ),
            )

            db.add(record)

        # -------------------------------------------------
        # MARK SCHEDULE AS COMPLETED
        # -------------------------------------------------

        schedule.schedule_status = "Completed"

        # -------------------------------------------------
        # EMPTY THE BIN
        # -------------------------------------------------

        if waste_bin:

            waste_bin.fill_level = 0

            waste_bin.bin_status = "Empty"

        # -------------------------------------------------
        # CREATE COMPLETION NOTIFICATION
        # -------------------------------------------------

        create_notification(
            user_id=schedule.user_id,

            title="Waste Collection Completed",

            message=(
                f"Collection for waste bin "
                f"#{schedule.bin_id} has been completed "
                f"successfully. The bin has been emptied."
            ),

            notification_type="Collection",

            db=db,
        )

        processed.append(
            schedule.schedule_id
        )

    # =====================================================
    # STEP 4 — SAVE EVERYTHING
    # =====================================================

    db.commit()

    return processeds