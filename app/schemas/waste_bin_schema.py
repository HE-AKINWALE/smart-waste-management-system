from pydantic import BaseModel, Field


class WasteBinCreate(BaseModel):
    bin_location: str
    capacity: float = Field(gt=0)
    fill_level: int = Field(ge=0, le=100)


class WasteBinUpdate(BaseModel):
    bin_location: str
    capacity: float = Field(gt=0)
    fill_level: int = Field(ge=0, le=100)


class WasteBinResponse(BaseModel):
    bin_id: int
    user_id: int | None
    bin_location: str
    capacity: float
    fill_level: int
    bin_status: str

    class Config:
        from_attributes = True