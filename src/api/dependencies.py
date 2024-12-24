from fastapi import Depends

from sqlalchemy.orm import Session

from src.db.db import get_db_session

from src.repositories.users import UserRepository
from src.services.users import UserService


# def users_service(session: Session = Depends(get_db_session)) -> UserService:
#     users_repository = UserRepository(session=session)
#     return UserService(users_repository)
