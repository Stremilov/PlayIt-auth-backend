from typing import Optional, List
from pydantic import BaseModel


# Input schemas
class UserCreateSchema(BaseModel):
    username: str
    telegram_id: int


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    telegram_id: Optional[int]
    balance: Optional[int] = 0
    done_tasks: Optional[int] = 0
    group_number: Optional[str]


class Prize(BaseModel):
    id: int
    title: str
    value: int


class UserSchema(BaseModel):
    id: int
    username: str
    full_name: str
    telegram_id: int
    balance: int
    done_tasks: List[int]
    group_number: Optional[str]
    prizes: Optional[List[Prize]] = []


class UpdatePersonalDataSchema(BaseModel):
    full_name: Optional[str]
    group_number: Optional[str]


# Output schemas for users end-points
class TelegramLoginResponse(BaseModel):
    status: str
    message: str


class BaseResponse(BaseModel):
    status: str
    message: str
    user: UserSchema


class UpdateUserBalanceData(BaseModel):
    task_id: int
    user_id: int
    value: int
    status: str
