from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )