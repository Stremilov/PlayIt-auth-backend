from fastapi import APIRouter, Depends
from typing import Annotated
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    TelegramLoginResponse
)
from src.services.users import UsersService
from src.api.dependencies import users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/telegram-login", response_model=TelegramLoginResponse)
async def telegram_login(
        user: UserCreateSchema,
        service: Annotated[UsersService, Depends(users_service)]
):
    existing_user = service.get_user_by_telegram_id(user.telegram_id)
    if existing_user:  # If existing user is not none
        return TelegramLoginResponse(
            status="success",
            message="Logged in",
            user=existing_user
        )

    created_user = service.create_user(user)
    return TelegramLoginResponse(
        status="success",
        message="Registered and logged in",
        user=created_user
    )
