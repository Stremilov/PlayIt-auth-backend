from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from uuid import UUID

from src.db.db import get_db_session
from src.schemas.sessions import (
    SessionData,
    GetUserRoleResponse
)
from src.sessions.backend import backend, cookie
from src.sessions.verifier import verifier
from src.services.users import UserService
from src.api.responses import sessions_role_responses
from src.utils.enums import RoleEnum

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    print(session_data)
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"


@router.get(
    path="/role",
    dependencies=[Depends(cookie)],
    response_model=GetUserRoleResponse,
    summary="Получить роль пользователя",
    description="""
    Возвращает роль текущего пользователя.

    - Использует данные текущей сессии.
    - Если пользователь найден, возвращает роль.
    - Если пользователь не найден, возвращает сообщение об ошибке.
    """,
    responses=sessions_role_responses
)
async def get_user_role(
        session: Session = Depends(get_db_session),
        session_data: SessionData = Depends(verifier)
):
    return await UserService.user_role(session=session, session_data=session_data)

