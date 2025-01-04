from typing import Optional, Union

from fastapi import HTTPException, Request
from fastapi import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from psycopg2.errors import UniqueViolation  # Оно есть, но Pycharm подчёркивает красным у меня о.О?

from src.repositories.users import UserRepository
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse,
    WhoamiResponse
)

from src.utils.enums import RoleEnum

from src.jwt.tokens import (
    create_jwt_token,
    verify_jwt_token
)


class UserService:
    @staticmethod
    async def auth_user(
            session: Session,
            response: Response,
            user: UserCreateSchema
    ):
        """
        Основной метод аутентификации пользователя:
        - Если пользователь существует, создаётся JWT-токен.
        - Если пользователь не существует, создаётся новый пользователь, а затем создаётся JWT-токен.
        """
        username = user.username
        telegram_id = user.telegram_id
        token = create_jwt_token(username, telegram_id)
        try:
            existing_user = UserRepository.get_user_by_username(session=session, username=username)
            if existing_user:
                response.set_cookie(key="jwt-token", value=token, httponly=True)
                return TelegramLoginResponse(
                    status="success",
                    message="Logged in"
                )

            users_dict = user.model_dump()
            new_user = UserRepository.create_user(session=session, data=users_dict)

            response.set_cookie(key="jwt-token", value=token, httponly=True)
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
                detail=f"Внутренняя ошибка базы данных: {e}"
                # Решил не выводить здесь с помощью str(e) полностью ошибку, так как она раскрывает все поля
                # базы данных, думаю так безопаснее
            )

    @staticmethod
    async def whoami(
            request: Request,
            session: Session
    ) -> WhoamiResponse:

        """
        Получает информацию о пользователе на основе JWT-токена.
        """
        try:
            token = request.cookies.get("jwt-token")
            if not token:
                raise HTTPException(status_code=401, detail="Не авторизован")

            verified_token = verify_jwt_token(token)

            username = verified_token.get("sub")
            user = UserRepository.get_user_by_username(session=session, username=username)

            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            return WhoamiResponse(
                status="success",
                message="Пользователь по этому jwt-токену найден.",
                user=user
            )
        except Exception as e:
            # Ловлю любые неожиданные ошибки
            raise HTTPException(
                status_code=500,
                detail=f"Произошла непредвиденная ошибка: {e}"
            )
