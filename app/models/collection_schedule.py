from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class CollectionSchedule(Base):
    __tablename__ = "collection_schedule"

    schedule_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    bin_id = Column(
        Integer,
        ForeignKey("waste_bins.bin_id")
    )

    collection_date = Column(
        Date
    )

    priority_level = Column(
        String(30)
    )

    schedule_status = Column(
        String(30),
        default="Pending"
    )

    # =====================================================
    # USER RELATIONSHIP
    # =====================================================

    user = relationship(
        "User",
        back_populates="collection_schedules"
    )

    # =====================================================
    # WASTE BIN RELATIONSHIP
    # =====================================================

    waste_bin = relationship(
        "WasteBin",
        back_populates="collection_schedules"
    )

    # =====================================================
    # COLLECTION RECORD RELATIONSHIP
    # =====================================================

    collection_record = relationship(
        "CollectionRecord",
        back_populates="schedule",
        uselist=False,
        cascade="all, delete-orphan"
    )