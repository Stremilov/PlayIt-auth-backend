from pydantic import BaseModel
from src.utils.enums import RoleEnum


class SessionData(BaseModel):
    username: str


# Output Schema
class GetUserRoleResponse(BaseModel):
    status: str
    message: str
    role: RoleEnum

    class Config:
        from_attributes = True
