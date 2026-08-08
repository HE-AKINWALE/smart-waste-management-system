from pydantic import BaseModel


class ReportSummary(BaseModel):

    total_users: int

    total_bins: int

    full_bins: int

    pending_collections: int

    completed_collections: int

    collection_efficiency: float


class AIReportResponse(BaseModel):

    summary: ReportSummary

    recommendations: list[str]