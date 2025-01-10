from fastapi import HTTPException, Request
from fastapi import Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from psycopg2.errors import UniqueViolation
from starlette import status

from src.repositories.users import UserRepository
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse,
    UpdatePersonalDataSchema, BaseResponse,
)
from src.utils.auth import verify_user_by_jwt


from src.jwt.tokens import (
    create_jwt_token,
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
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Пользователь с таким telegram_id уже существует"
                )

        except Exception as e:
            # Ловлю любые неожиданные ошибки
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка базы данных: {e}"
                # Решил не выводить здесь с помощью str(e) полностью ошибку, так как она раскрывает все поля
                # базы данных, думаю так безопаснее
            )

    @staticmethod
    async def get_user_info(
            request: Request,
            session: Session
    ) -> BaseResponse:

        """
        Получает информацию о пользователе на основе JWT-токена.
        """
        try:
            user = await verify_user_by_jwt(request, session)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

            return BaseResponse(
                status="success",
                message="Пользователь по этому jwt-токену найден.",
                user=user
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла непредвиденная ошибка: {e}"
            )

    @staticmethod
    async def manage_user_balance(
            request: Request,
            session: Session,
            value: int
    ) -> BaseResponse:
        """
        Получает значение и изменяет баланс пользователя на это значение
        """
        try:
            user = await verify_user_by_jwt(request, session)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

            user = UserRepository.update_user_balance(session, user.username, value)

            return BaseResponse(
                status="success",
                message="Баланс пользователя успешно обновлен",
                user=user
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла непредвиденная ошибка: {e}"
            )

    @staticmethod
    async def update_user_personal_data(
            request: Request,
            session: Session,
            new_data: UpdatePersonalDataSchema,
    ) -> BaseResponse:
        """
        Получает значение и изменяет баланс пользователя на это значение
        """
        try:
            if not new_data.full_name and not new_data.group_number:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пустое тело запроса")

            user = await verify_user_by_jwt(request, session)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

            user = UserRepository.update_user_personal_data(session, user.username, new_data)

            return BaseResponse(
                status="success",
                message="Данные пользователя успешно обновлены",
                user=user
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла непредвиденная ошибка: {e}"
            )
