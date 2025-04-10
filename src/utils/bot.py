import logging
import os

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.models import Users

from aiogram import Bot


bot = Bot(token=os.getenv("TOKEN"))


async def notify_user_task_checked(session: Session, user_id: int):
    stmt = select(Users).where(Users.id == user_id)
    result = session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not user.telegram_id:
        return

    message = "Задание твоё проверено! Пожалуй, поспеши узреть, что там да как!\nЗаходи да смотри!"

    try:
        await bot.send_message(chat_id=user.telegram_id, text=message)
    except Exception as e:
        logging.warning(f"Не удалось отправить сообщение пользователю {user.telegram_id}: {e}")
