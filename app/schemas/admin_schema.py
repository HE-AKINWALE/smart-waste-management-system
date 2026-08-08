from pydantic import BaseModel


class SystemSummary(BaseModel):
    total_users: int
    total_bins: int
    total_schedules: int
    total_completed_collections: int
    total_notifications: int