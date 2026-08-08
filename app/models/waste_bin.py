from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class WasteBin(Base):
    __tablename__ = "waste_bins"

    bin_id = Column(Integer, primary_key=True, index=True)
    bin_location = Column(String(255), nullable=False)
    capacity = Column(Float, nullable=False)
    fill_level = Column(Integer, default=0)
    bin_status = Column(String(50), default="Empty")