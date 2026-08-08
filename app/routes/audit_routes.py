from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.schemas.audit_schema import (
    AuditLogCreate,
    AuditLogResponse
)

from app.services.audit_service import (
    create_audit_log,
    get_all_logs,
    get_user_logs
)

router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/",
    response_model=AuditLogResponse
)
def add_log(
    audit: AuditLogCreate,
    db: Session = Depends(get_db)
):

    return create_audit_log(
        audit,
        db
    )


@router.get(
    "/",
    response_model=list[AuditLogResponse]
)
def all_logs(
    db: Session = Depends(get_db)
):

    return get_all_logs(db)


@router.get(
    "/user/{user_id}",
    response_model=list[AuditLogResponse]
)
def logs_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_user_logs(
        user_id,
        db
    )