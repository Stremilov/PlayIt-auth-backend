from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from typing import Optional

from src.models.models import Users
from src.schemas.users import UserSchema


class UserRepository:
    @staticmethod
    def create_user(session: Session, data: dict) -> UserSchema:
        statement = insert(Users).values(**data).returning(Users)
        result = session.execute(statement)
        session.commit()

        created_user = result.scalars().first()
        new_user = created_user.to_read_model()
        return new_user

    @staticmethod
    def get_user_by_username(session: Session, username: str) -> Optional[UserSchema]:
        statement = select(Users).filter_by(username=username)
        result = session.execute(statement)

        user = result.scalar_one_or_none()
        if not user:
            return None
        return user.to_read_model()

    @staticmethod
    def update_user_balance(session: Session, username: str, value: int):
        statement = update(Users).where(Users.username == username).values(balance=Users.balance + value)
        session.execute(statement)
        session.commit()

        statement = select(Users).filter_by(username=username)
        result = session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return None
        return user.to_read_model()
