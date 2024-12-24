from http.client import HTTPResponse

from fastapi import APIRouter, Depends, Response
from typing import Annotated

from src.db.db import get_db_session
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse
)
from src.services.users import UserService
# from src.api.dependencies import users_service
from src.utils.auth import login

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/telegram-login",
    response_model=TelegramLoginResponse,
    summary="Авторизует пользователя",
    description="""
    Создает полноценный аккаунт

    - Создает/проверяет пользователя 
    - Отправляет в cookie токен доступа для сессии
    - Создает запись в базе данных
    """,
    responses={
        200: {
            "status": "success",
            "message": "Logged in",
        },
        500: {
            "description": "Внутренняя ошибка",
        },
    },
)
async def telegram_login(
        user: UserCreateSchema,
        session: Depends(get_db_session),
        response: Response
):
    return await UserService.auth_user(session=session, response=response, user=user)
