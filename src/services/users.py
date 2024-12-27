from typing import Optional, Union

from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from psycopg2.errors import UniqueViolation  # Оно есть, но Pycharm подчёркивает красным у меня о.О?

from src.repositories.users import UserRepository
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse
)
from src.schemas.sessions import (
    GetUserRoleResponse,
    SessionData
)

from src.utils.auth import login
from src.utils.enums import RoleEnum


class UserService:
    @staticmethod
    async def auth_user(
            session: Session,
            response: Response,
            user: UserCreateSchema
    ) -> Optional[TelegramLoginResponse]:
        """
        Основной метод аутентификации пользователя:
        - Если пользователь существует, выполняется логин.
        - Если пользователь не существует, создаётся новый пользователь, а затем выполняется логин.
        """

        # Так как довольно часто используем тут user.username решил вывести её в отдельную переменную
        username = user.username

        try:
            # Проверка существует ли пользователь
            existing_user = UserRepository.get_user_by_username(session=session, username=username)
            if existing_user:  # Если пользователь существует
                # Если пользователь существует, выполняем логин
                await UserService._login_user(response=response, username=username)
                return TelegramLoginResponse(
                    status="success",
                    message="Logged in"
                )

            # Если пользователь не существует, то создаём его
            users_dict = user.model_dump()  # Перевожу UserCreateSchema в dict
            created_user = UserRepository.create_user(session=session, data=users_dict)

            # Логин для нового пользователя
            await UserService._login_user(response=response, username=username)
            return TelegramLoginResponse(
                status="success",
                message="Registered and logged in"
            )

        except IntegrityError as e:
            # Проверяю, связана ли ошибка с уникальностью telegram_id
            # Не проверяю связана ли с username'ом, так как ранее делал проверку существует ли пользователь
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(
                    status_code=409,
                    detail="Пользователь с таким telegram_id уже существует"
                )

        except Exception as e:
            # Ловлю любые неожиданные ошибки
            raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка базы данных: {type(e)}"
                # Решил не выводить здесь с помощью str(e) полностью ошибку, так как она раскрывает все поля
                # базы данных, думаю так безопаснее
            )

    @staticmethod
    async def _login_user(response: Response, username: str) -> None:
        """Защищённый метод для логина пользователя"""
        try:
            await login(response=response, name=username)
        except ValueError as e:
            # Если придут ошибки при авторизации в src/utils/auth
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка авторизации: {str(e)}"
            )

        except Exception as e:
            # Для неожиданных ошибок
            raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка при авторизации: {str(e)}"
            )

    @staticmethod
    async def user_role(
            session: Session,
            session_data: SessionData
    ) -> GetUserRoleResponse:
        try:
            username = session_data.username
            existing_user = UserRepository.get_user_by_username(session=session, username=username)
            if existing_user:  # Если пользователь существует
                # Если пользователь существует, отдаём роль
                return GetUserRoleResponse(
                    status="success",
                    message=f"Роль пользователя: '{username}' получена",
                    role=RoleEnum(existing_user.role)
                )
            # Если пользователь не найден, отдаю 404
            raise HTTPException(
                status_code=404,
                detail={
                    "status": "failed",
                    "message": f"Пользователь с именем: '{username}' не существует"
                }
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"Внутренняя ошибка сервера: {str(e)}"
            )
