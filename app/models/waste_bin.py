from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class WasteBin(Base):
    __tablename__ = "waste_bins"

    bin_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=True,
        index=True
    )

    bin_location = Column(
        String(255),
        nullable=False
    )

    capacity = Column(
        Float,
        nullable=False
    )

    fill_level = Column(
        Integer,
        nullable=True
    )

    bin_status = Column(
        String(50),
        nullable=True
    )

    # -------------------------------------------------
    # RELATIONSHIPS
    # -------------------------------------------------

    user = relationship(
        "User",
        back_populates="waste_bins"
    )

    collection_schedules = relationship(
        "CollectionSchedule",
        back_populates="waste_bin"
    )