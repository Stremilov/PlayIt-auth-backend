import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from src.db.db import Base, get_db_session
from main import app
import os

# Настройка тестовой базы данных
DATABASE_URL = "postgresql://postgres:1234@localhost/test_db"  # Создайте БД с именем test_db в PGAdmin4 (Любой другой СУБД)
# перед запуском тестов либо поменяйте тут параметры
engine_test = create_engine(DATABASE_URL, future=True)
TestSession = sessionmaker(bind=engine_test, expire_on_commit=False)


# Фикстура для базы данных
@pytest.fixture(autouse=True)
def prepare_database():
    """Подготовка тестовой базы данных перед каждым тестом."""
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


# Фикстура для замены зависимости get_db_session
@pytest.fixture
def override_get_db_session():
    """Замена зависимости для получения сессии базы данных."""

    def _override():
        with TestSession() as session:
            yield session

    app.dependency_overrides[get_db_session] = _override


# Фикстура для асинхронного клиента
@pytest_asyncio.fixture
async def client(override_get_db_session):
    """Асинхронный клиент для тестирования."""
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac
