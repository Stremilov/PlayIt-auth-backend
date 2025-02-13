from sqlalchemy import Column, Integer, String, DateTime, Enum, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime

from src.db.db import Base

from src.schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False)
    full_name = Column(String, default="", nullable=False)
    telegram_id = Column(Integer, unique=True, nullable=True)
    balance = Column(Integer, default=0, nullable=False)
    done_tasks = Column(ARRAY(Integer), default=list, nullable=True)
    group_number = Column(String, default="", nullable=True)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            telegram_id=self.telegram_id,
            balance=self.balance,
            done_tasks=self.done_tasks,
            group_number=self.group_number
        )


class Transactions(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    transaction_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Перевод в transaction схему не сделал, т.к. не понятно, нужно ли ещё делать схемы для transaction
