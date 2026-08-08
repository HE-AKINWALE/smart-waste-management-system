from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.schemas.audit_schema import AuditLogCreate


def create_audit_log(
    audit: AuditLogCreate,
    db: Session
):

    new_log = AuditLog(
        user_id=audit.user_id,
        activity=audit.activity,
        module=audit.module,
        ip_address=audit.ip_address
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


def get_all_logs(db: Session):

    return db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).all()


def get_user_logs(
    user_id: int,
    db: Session
):

    return db.query(AuditLog).filter(
        AuditLog.user_id == user_id
    ).all()