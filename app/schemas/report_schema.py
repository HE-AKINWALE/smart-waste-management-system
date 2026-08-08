from pydantic import BaseModel


class DashboardReport(BaseModel):
    total_users: int
    total_bins: int
    active_bins: int
    full_bins: int
    pending_schedules: int
    completed_collections: int
    total_notifications: int
    collection_efficiency: float

class BinStatusReport(BaseModel):
    active_bins: int
    inactive_bins: int
    full_bins: int


class FillLevelReport(BaseModel):
    low: int
    medium: int
    high: int
    critical: int


class SystemHealthReport(BaseModel):
    collection_efficiency: float
    notification_count: int
    pending_schedules: int
    completed_collections: int