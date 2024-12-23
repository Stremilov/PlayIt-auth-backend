from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

from src.db.db import Base
from src.utils.enums import RoleEnum, StatusEnum

from src.schemas.users import UserSchema  # For to_read_model function
from src.schemas.tasks import TaskSchema


class CustomUser(Base):
    __tablename__ = "custom_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            password=self.password,
            telegram_id=self.telegram_id,
            role=self.role
        )


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("custom_user.id"), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("CustomUser", back_populates="tasks")

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id,
            user_id=self.user_id,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
