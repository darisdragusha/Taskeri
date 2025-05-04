from pydantic import BaseModel

class PermissionCreate(BaseModel):
    name: str

class PermissionUpdate(BaseModel):
    name: str

class PermissionResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
