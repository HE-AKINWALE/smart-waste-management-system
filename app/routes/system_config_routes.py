from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.system_config_schema import (
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigResponse
)

from app.services.system_config_service import (
    create_config,
    get_all_configs,
    get_config,
    update_config,
    delete_config
)

router = APIRouter(
    prefix="/system-config",
    tags=["System Configuration"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/",
    response_model=SystemConfigResponse
)
def add_config(
    config: SystemConfigCreate,
    db: Session = Depends(get_db)
):

    return create_config(config, db)


@router.get(
    "/",
    response_model=list[SystemConfigResponse]
)
def all_configs(
    db: Session = Depends(get_db)
):

    return get_all_configs(db)


@router.get(
    "/{config_id}",
    response_model=SystemConfigResponse
)
def one_config(
    config_id: int,
    db: Session = Depends(get_db)
):

    config = get_config(config_id, db)

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found."
        )

    return config


@router.put(
    "/{config_id}",
    response_model=SystemConfigResponse
)
def edit_config(
    config_id: int,
    data: SystemConfigUpdate,
    db: Session = Depends(get_db)
):

    config = update_config(
        config_id,
        data,
        db
    )

    if not config:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found."
        )

    return config


@router.delete("/{config_id}")
def remove_config(
    config_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_config(
        config_id,
        db
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found."
        )

    return {
        "message": "Configuration deleted successfully."
    }