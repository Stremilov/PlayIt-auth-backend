from typing import Optional
from pydantic import BaseModel
from src.utils.enums import RoleEnum


# Input schemas
class UserCreateSchema(BaseModel):
    username: str
    telegram_id: int


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    telegram_id: Optional[int]
    balance: Optional[int] = 0
    role: Optional[RoleEnum]
    done_tasks: Optional[int] = 0
    group_number: Optional[str]


class UserSchema(BaseModel):
    id: int
    username: str
    telegram_id: int
    balance: int
    role: RoleEnum
    done_tasks: int
    group_number: str

    class Config:
        from_attributes = True


# Output schemas for users end-points
class TelegramLoginResponse(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True


class WhoamiResponse(BaseModel):
    status: str
    message: str
    user: UserSchema