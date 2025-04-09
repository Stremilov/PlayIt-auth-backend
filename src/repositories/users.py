import logging

from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import insert, select, update, func
from typing import Optional

from src.models.models import Users
from src.schemas.users import UserSchema, UpdatePersonalDataSchema


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
        statement = select(Users).options(joinedload(Users.prizes)).filter_by(username=username)
        result = session.execute(statement).unique()

        user = result.scalar_one_or_none()
        if not user:
            return None

        return user.to_read_model()

    @staticmethod
    def update_user_balance(session: Session, user_id: int, value: int, task_id: int):
        user_check_stmt = select(Users.in_progress).where(Users.id == user_id)
        result = session.execute(user_check_stmt)
        user_in_progress = result.scalar_one_or_none()

        if user_in_progress and task_id in user_in_progress:
            remove_task_stmt = update(Users).where(Users.id == user_id).values(
                in_progress=func.array_remove(Users.in_progress, task_id)
            )
            session.execute(remove_task_stmt)
            logging.debug(f"Удален task_id {task_id} из in_progress.")

            update_done_tasks_stmt = update(Users).where(Users.id == user_id).values(
                done_tasks=func.array_append(Users.done_tasks, task_id)
            )
            session.execute(update_done_tasks_stmt)
            logging.debug(f"Добавлен task_id {task_id} в done_tasks.")

        statement = update(Users).where(Users.id == user_id).values(balance=Users.balance + value)
        result = session.execute(statement)
        logging.debug(result)

        update_tasks_stmt = (
            update(Users)
            .where(Users.id == user_id)
            .values(done_tasks=func.array_append(Users.done_tasks, task_id))
        )
        result = session.execute(update_tasks_stmt)
        logging.debug(result)

        session.commit()

        statement = select(Users).filter_by(id=user_id)
        result = session.execute(statement)
        logging.debug(result)

        user = result.scalar_one_or_none()

        if not user:
            return None
        return user.to_read_model()

    @staticmethod
    def update_user_personal_data(session: Session, username: str, new_data: UpdatePersonalDataSchema):
        update_values = {}

        if new_data.full_name is not None and new_data.full_name != "":
            update_values['full_name'] = new_data.full_name

        if new_data.group_number is not None and new_data.group_number != "":
            update_values['group_number'] = new_data.group_number

        statement = update(Users).where(Users.username == username).values(**update_values)
        session.execute(statement)
        session.commit()

        statement = select(Users).filter_by(username=username)
        result = session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return None
        return user.to_read_model()

    @staticmethod
    def delete_task_from_in_progress(session: Session, user_id: int, task_id: int):
        user_check_stmt = select(Users.in_progress).where(Users.id == user_id)
        result = session.execute(user_check_stmt)
        user_in_progress = result.scalar_one_or_none()

        if user_in_progress and task_id in user_in_progress:
            remove_task_stmt = update(Users).where(Users.id == user_id).values(
                in_progress=func.array_remove(Users.in_progress, task_id)
            )
            session.execute(remove_task_stmt)
            logging.debug(f"Удален task_id {task_id} из in_progress.")

        statement = select(Users).filter_by(id=user_id)
        result = session.execute(statement)
        logging.debug(result)

        user = result.scalar_one_or_none()

        if not user:
            return None
        return user.to_read_model()