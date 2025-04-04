from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

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

    prizes = relationship("Prize", back_populates="user")

    def to_read_model(self) -> UserSchema:
        prizes_data = [{"id": p.id, "title": p.title, "value": p.value} for p in self.prizes]
        return UserSchema(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            telegram_id=self.telegram_id,
            balance=self.balance,
            done_tasks=self.done_tasks,
            group_number=self.group_number,
            prizes=prizes_data
        )


class Prize(Base):
    __tablename__ = "prizes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    value = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="prizes")
    # Перевод в transaction схему не сделал, т.к. не понятно, нужно ли ещё делать схемы для transaction
