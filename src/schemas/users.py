from typing import Optional
from pydantic import BaseModel, EmailStr
from src.utils.enums import RoleEnum


# Input schemas
class UserCreateSchema(BaseModel):
    username: str
    password: str
    # email: EmailStr
    telegram_id: int
    role: RoleEnum


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    # email: Optional[EmailStr]
    telegram_id: Optional[int]
    role: Optional[RoleEnum]


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    # email: EmailStr
    telegram_id: int
    role: RoleEnum

    class Config:
        from_attributes = True


# Output schemas for users end-points
class TelegramLoginResponse(BaseModel):
    status: str
    message: str
    user: UserSchema

    class Config:
        from_attributes = True


class GetUserRoleResponse(BaseModel):
    status: str
    message: str
    role: RoleEnum

    class Config:
        from_attributes = True
