from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.report_schema import DashboardReport
from app.services.report_service import dashboard_report

from app.schemas.report_schema import (
    DashboardReport,
    BinStatusReport,
    FillLevelReport,
    SystemHealthReport
)

from app.services.report_service import (
    dashboard_report,
    bin_status_report,
    fill_level_distribution,
    critical_bins,
    weekly_schedule,
    monthly_collections,
    system_health
)

from app.schemas.waste_bin_schema import WasteBinResponse
from app.schemas.schedule_schema import CollectionScheduleResponse
from app.schemas.record_schema import CollectionRecordResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/dashboard",
    response_model=DashboardReport
)
def dashboard(
    db: Session = Depends(get_db)
):
    return dashboard_report(db)

@router.get("/bin-status", response_model=BinStatusReport)
def bin_status(db: Session = Depends(get_db)):
    return bin_status_report(db)


@router.get("/fill-levels", response_model=FillLevelReport)
def fill_levels(db: Session = Depends(get_db)):
    return fill_level_distribution(db)


@router.get("/critical-bins", response_model=list[WasteBinResponse])
def critical(db: Session = Depends(get_db)):
    return critical_bins(db)


@router.get("/weekly-schedule", response_model=list[CollectionScheduleResponse])
def weekly(db: Session = Depends(get_db)):
    return weekly_schedule(db)


@router.get("/monthly-collections", response_model=list[CollectionRecordResponse])
def monthly(db: Session = Depends(get_db)):
    return monthly_collections(db)


@router.get("/system-health", response_model=SystemHealthReport)
def health(db: Session = Depends(get_db)):
    return system_health(db)