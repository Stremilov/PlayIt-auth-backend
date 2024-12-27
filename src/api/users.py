from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.db.db import get_db_session
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse
)
from src.services.users import UserService
from src.api.responses import telegram_login_responses

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    path="/telegram-login",
    response_model=TelegramLoginResponse,
    summary="Авторизует пользователя",
    description="""
    Создает полноценный аккаунт

    - Создает/проверяет пользователя 
    - Отправляет в cookie токен доступа для сессии
    - Создает запись в базе данных
    """,
    responses=telegram_login_responses
)
async def telegram_login(
        user: UserCreateSchema,
        response: Response,
        session: Session = Depends(get_db_session)  # Указываю Session из SQLALchemy.orm, чтобы не возникала ошибка
):
    return await UserService.auth_user(session=session, response=response, user=user)
