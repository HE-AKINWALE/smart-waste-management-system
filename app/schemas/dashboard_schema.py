from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_users: int

    total_bins: int

    bins_requiring_collection: int

    pending_collections: int

    completed_collections: int

    collection_efficiency: float

    system_health: str