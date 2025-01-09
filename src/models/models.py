from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from src.db.db import Base
from src.utils.enums import RoleEnum, StatusEnum

from src.schemas.users import UserSchema  # For to_read_model function
from src.schemas.tasks import TaskSchema


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    users = relationship("Users", back_populates="tasks")

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            user_id=self.user_id,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=True)
    balance = Column(Integer, default=0, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    done_tasks = Column(Integer, default=0, nullable=False)
    group_number = Column(String, default="", nullable=False)

    tasks = relationship("Tasks", back_populates="users", cascade="all, delete-orphan")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            telegram_id=self.telegram_id,
            balance=self.balance,
            role=self.role,
            done_tasks=self.done_tasks,
            group_number=self.group_number
        )


class Transactions(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    transaction_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Перевод в transaction схему не сделал, т.к. не понятно, нужно ли ещё делать схемы для transaction
