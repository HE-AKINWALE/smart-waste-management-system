from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class CollectionRecord(Base):
    __tablename__ = "collection_records"

    record_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    schedule_id = Column(
        Integer,
        ForeignKey("collection_schedule.schedule_id"),
        unique=True,
        nullable=True
    )

    completion_date = Column(
        Date,
        nullable=False
    )

    collection_status = Column(
        String(30),
        default="Completed",
        nullable=True
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    schedule = relationship(
        "CollectionSchedule",
        back_populates="collection_record"
    )