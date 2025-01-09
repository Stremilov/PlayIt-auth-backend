from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import logging

# Database configuration for connection
DATABASE_URL = f"postgresql://postgres:sdgdfs13@localhost:5432/playit"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# Base class for models in src/models/models.py
class Base(DeclarativeBase):
    pass


def init_db():
    with engine.begin() as conn:
        logging.info("Создаю таблицы POSTGRESQL!")
        Base.metadata.create_all(bind=conn)
    logging.info("Таблицы созданы!")


# Synchronous sessions generator
def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
