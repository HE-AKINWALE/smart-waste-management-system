from pydantic import BaseModel


class SystemConfigCreate(BaseModel):

    config_key: str

    config_value: str

    description: str


class SystemConfigUpdate(BaseModel):

    config_value: str


class SystemConfigResponse(BaseModel):

    config_id: int

    config_key: str

    config_value: str

    description: str

    model_config = {
        "from_attributes": True
    }