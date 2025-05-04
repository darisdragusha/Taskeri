from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name: str

class PermissionUpdate(BaseModel):
    name: str

class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }