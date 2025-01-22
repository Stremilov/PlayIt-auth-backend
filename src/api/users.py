from fastapi import APIRouter, Depends, Response, Request, Cookie
from sqlalchemy.orm import Session

from src.db.db import get_db_session
from src.schemas.users import (
    UserCreateSchema,
    TelegramLoginResponse,
    UpdatePersonalDataSchema, BaseResponse
)
from src.services.users import UserService
from src.api.responses import (
    telegram_login_responses,
    whoami_responses, update_user_balance_responses, update_user_personal_data_responses
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    path="/telegram-login",
    response_model=TelegramLoginResponse,
    summary="Авторизует пользователя",
    description="""
    Создает полноценный аккаунт:

    - Создает/проверяет пользователя;
    - Отправляет в cookie JWT-токен доступа;
    - Если пользователя не существовало, то создаёт запись в базе данных.
    """,
    responses=telegram_login_responses
)
async def telegram_login(
        user: UserCreateSchema,
        response: Response,
        session: Session = Depends(get_db_session)
):
    return await UserService.auth_user(session=session, response=response, user=user)


@router.get(
    path="/whoami",
    response_model=BaseResponse,
    summary="Информация о текущем пользователе",
    description="""
    Возвращает информацию о текущем пользователе на основе JWT токена:
    
    - Проверяет наличие токена в куки, если его не будет, то вернёт 401 HTTP status_code;
    - Декодирует и проверяет JWT-токен, если он некорректен, то вернёт 401 HTTP status_code;
    - Ищет пользователя по username из JWT-токена в базе данных, если не находит, то возвращает 404 HTTP status_code;
    - Возвращает данные пользователя из базы данных.
    """,
    responses=whoami_responses
)
async def whoami(
        request: Request,
        session: Session = Depends(get_db_session)
):
    return await UserService.get_user_info(request=request, session=session)


@router.put(
    path="/balance/{value}",
    response_model=BaseResponse,
    summary="Изменение баланса пользователя",
    description="""
    Изменяет баланс пользователю (как в положительную так и отрицательную сторону) и возвращает всего пользователя
    
    - Проверяет наличие токена в куки, если его не будет, то вернёт 401 HTTP status_code;
    - Декодирует и проверяет JWT-токен, если он некорректен, то вернёт 401 HTTP status_code;
    - Ищет пользователя по username из JWT-токена в базе данных, если не находит, то возвращает 404 HTTP status_code;
    - Изменяет баланс пользователя как в положительную так и отрицательную сторону (нужно передать или 100 или -100 к примеру)
    - Возвращает все данные пользователя
    """,
    responses=update_user_balance_responses
)
async def manage_balance(
        value: int,
        request: Request,
        session: Session = Depends(get_db_session),
):
    return await UserService.manage_user_balance(request=request, session=session, value=value)


@router.put(
    path="/personal-data",
    response_model=BaseResponse,
    summary="Изменение личной информации о пользователе",
    description="""
    Изменяет персональные данные пользователя (ФИО и номер группы) и возвращает всего пользователя

    - Проверяет наличие токена в куки, если его не будет, то вернёт 401 HTTP status_code;
    - Декодирует и проверяет JWT-токен, если он некорректен, то вернёт 401 HTTP status_code;
    - Ищет пользователя по username из JWT-токена в базе данных, если не находит, то возвращает 404 HTTP status_code;
    - Если приходит пустое тело, то возвращает 400 HTTP status_code;
    - Изменяет личные данные пользователя: ФИО, номер группы. К примеру на Иванов Иван Иванович, ИСТ-000;
    - Возвращает все данные пользователя
    """,
    responses=update_user_personal_data_responses
)
async def update_personal_user_data(
        new_data: UpdatePersonalDataSchema,
        request: Request,
        session: Session = Depends(get_db_session),
):
    return await UserService.update_user_personal_data(request=request, session=session, new_data=new_data)

