from sqlalchemy import Column, Integer, String

from app.database.database import Base


class SystemConfig(Base):
    __tablename__ = "system_config"

    config_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    config_key = Column(
        String(100),
        unique=True,
        nullable=False
    )

    config_value = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(255)
    )