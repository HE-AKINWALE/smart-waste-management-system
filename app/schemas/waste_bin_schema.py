from pydantic import BaseModel


class WasteBinCreate(BaseModel):
    bin_location: str
    capacity: float
    fill_level: int
    bin_status: str

class WasteBinUpdate(BaseModel):
    bin_location: str
    capacity: float
    fill_level: int

class WasteBinResponse(BaseModel):
    bin_id: int
    bin_location: str
    capacity: float
    fill_level: int
    bin_status: str

    class Config:
        from_attributes = True