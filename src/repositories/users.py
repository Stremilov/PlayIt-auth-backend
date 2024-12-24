from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from typing import List, Optional

from src.models.models import CustomUser
from src.schemas.users import UserSchema
from src.utils.enums import RoleEnum


class UserRepository:

    # Async or synchronous session for db here

    @staticmethod
    def create_user(session: Session, data: dict) -> UserSchema:
        statement = insert(CustomUser).values(**data).returning(CustomUser)
        result = session.execute(statement)
        session.commit()

        created_user = result.scalars().first()
        new_user = created_user.to_read_model()
        return new_user


    #
    # def get_by_user_id(self, user_id: int) -> Optional[UserSchema]:
    #     statement = select(self.model).filter_by(id=user_id)
    #     result = self.session.execute(statement)
    #
    #     user = result.scalar_one_or_none()
    #     if not user:
    #         return None  # Return None if no user is found
    #     return user.to_read_model()  # Return UserSchema with user info
    #
    # def get_all(self) -> List[UserSchema]:
    #     statement = select(self.model)
    #     result = self.session.execute(statement)
    #
    #     all_users = [user.to_read_model() for user in result.scalars().all()]  # List of UserSchemas
    #     return all_users
    #
    # def edit_one(self, user_id: int, data: dict) -> int:
    #     statement = update(self.model).values(**data).filter_by(id=user_id).returning(self.model.id)
    #     result = self.session.execute(statement)
    #     self.session.commit()
    #
    #     edited_user = result.scalars().first()
    #     return edited_user.to_read_model()
    #
    # def delete_one(self, user_id: int) -> int:
    #     statement = delete(self.model).where(self.model.id == user_id).returning(self.model.id)
    #     result = self.session.execute(statement)
    #     self.session.commit()
    #
    #     deleted_user_id = result.scalar_one()
    #     return deleted_user_id
    #
    # def get_one_by_filter(self, **filter_by):
    #     statement = select(self.model).filter_by(**filter_by)
    #     result = self.session.execute(statement)
    #
    #     user = result.scalar_one_or_none()
    #     if not user:
    #         return None
    #     return user.to_read_model()
