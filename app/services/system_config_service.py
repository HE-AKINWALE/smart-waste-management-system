from sqlalchemy.orm import Session

from app.models.system_config import SystemConfig
from app.schemas.system_config_schema import (
    SystemConfigCreate,
    SystemConfigUpdate
)


def create_config(
    config: SystemConfigCreate,
    db: Session
):

    new_config = SystemConfig(
        config_key=config.config_key,
        config_value=config.config_value,
        description=config.description
    )

    db.add(new_config)
    db.commit()
    db.refresh(new_config)

    return new_config


def get_all_configs(db: Session):

    return db.query(SystemConfig).all()


def get_config(
    config_id: int,
    db: Session
):

    return db.query(SystemConfig).filter(
        SystemConfig.config_id == config_id
    ).first()


def update_config(
    config_id: int,
    data: SystemConfigUpdate,
    db: Session
):

    config = get_config(config_id, db)

    if not config:
        return None

    config.config_value = data.config_value

    db.commit()
    db.refresh(config)

    return config


def delete_config(
    config_id: int,
    db: Session
):

    config = get_config(config_id, db)

    if not config:
        return False

    db.delete(config)
    db.commit()

    return True