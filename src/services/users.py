from typing import List, Optional

from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.orm import Session

from src.repositories.users import UserRepository
from src.schemas.users import (
    UserCreateSchema,
    UserUpdateSchema,
    UserSchema, TelegramLoginResponse
)
from src.utils.auth import login


class UserService:

    @staticmethod
    async def auth_user(session: Session, response: Response, user):
        try:
            existing_user = UserRepository.get_user_by_username(user.username)
            if existing_user:  # If existing user is not none
                try:
                    await login(response, user.username)
                    return TelegramLoginResponse(
                        status="success",
                        message="Logged in",
                        user=existing_user  # TODO убрать возврат юзера. Оно нам пока не надо
                    )
                except:
                    raise HTTPException(status_code=400, detail="Неверные данные для выполнения запроса")

            created_user = UserRepository.create_user(session, user)
            try:
                await login(response, user.username)
                return TelegramLoginResponse(
                    status="success",
                    message="Registered and logged in",
                    user=created_user  # TODO убрать возврат юзера. Оно нам пока не надо
                )
            except:
                raise HTTPException(status_code=400, detail="Неверные данные для выполнения запроса")
        except:
            raise HTTPException(status_code=500, detail="Внутренняя ошибка")

    #         pass
    #
    # def create_user(self, user: UserCreateSchema) -> UserSchema:
    #     users_dict = user.model_dump()
    #     created_user = self.users_repo.create_one(users_dict)
    #     return created_user
    #
    # def get_user_by_user_id(self, user_id: int) -> Optional[UserSchema]:
    #     user = self.users_repo.get_by_user_id(user_id)
    #     return user
    #
    # def get_all_users(self) -> List[UserSchema]:
    #     all_users = self.users_repo.get_all()
    #     return all_users
    #
    # def get_user_by_telegram_id(self, telegram_id: int) -> Optional[UserSchema]:
    #     user = self.users_repo.get_one_by_filter(telegram_id=telegram_id)
    #     return user
    #
    # def get_user_by_username(self, username: str) -> Optional[UserSchema]:
    #     user = self.users_repo.get_one_by_filter(username=username)
    #     return user
    #
    # def update_user_by_user_id(self, user_id: int, user: UserUpdateSchema) -> Optional[UserSchema]:
    #     # TODO: add check for user existance logic
    #
    #     updated_user = self.users_repo.edit_one(user_id, user)
    #     return updated_user
    #
    # def delete_user_by_user_id(self, user_id: int) -> int:
    #     deleted_user_id = self.users_repo.delete_one(user_id)
    #     return deleted_user_id
