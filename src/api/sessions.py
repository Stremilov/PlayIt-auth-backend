from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated
from uuid import UUID, uuid4
from src.schemas.sessions import (
    SessionData,
    GetUserRoleResponse
)
from src.sessions.backend import backend, cookie
from src.sessions.verifier import verifier

from src.services.users import UsersService
from src.api.dependencies import users_service


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


@router.post("/create_session/{name}")
async def create_session(name: str, response: Response):
    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"


@router.get("/role", dependencies=[Depends(cookie)], response_model=GetUserRoleResponse)
async def get_user_role(
        service: Annotated[UsersService, Depends(users_service)],
        session_data: SessionData = Depends(verifier)
):
    users_role = service.get_user_role_by_username(session_data.username)
    if users_role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserRoleResponse(
        status="success",
        message="User's role retrieved",
        role=users_role
    )
