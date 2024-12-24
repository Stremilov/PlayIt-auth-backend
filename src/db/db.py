from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import logging

# Database configuration for connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# Base class for models in src/models/models.py
class Base(DeclarativeBase):
    pass


def init_db():
    with engine.begin() as conn:
        logging.info("Creating tables POSTGRESQL!")
        Base.metadata.create_all(bind=conn)
    logging.info("Tables created!")


# Synchronous sessions generator
def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
