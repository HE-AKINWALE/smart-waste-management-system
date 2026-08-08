from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class CollectionSchedule(Base):
    __tablename__ = "collection_schedule"

    schedule_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    bin_id = Column(
        Integer,
        ForeignKey("waste_bins.bin_id")
    )

    collection_date = Column(Date)

    priority_level = Column(String(30))

    schedule_status = Column(
        String(30),
        default="Pending"
    )

    user = relationship("User")
    waste_bin = relationship("WasteBin")