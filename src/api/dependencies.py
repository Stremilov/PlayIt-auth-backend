from fastapi import Depends

from sqlalchemy.orm import Session

from src.db.db import get_db_session

from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service(session: Session = Depends(get_db_session)) -> UsersService:
    users_repository = UsersRepository(session=session)
    return UsersService(users_repository)
