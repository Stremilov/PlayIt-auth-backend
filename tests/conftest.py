import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.db import Base, get_db_session
from main import app
import uvicorn
from multiprocessing import Process

# Настройка тестовой базы данных
DATABASE_URL = "postgresql://postgres:1234@localhost/test_db"
engine_test = create_engine(DATABASE_URL, future=True)
TestSession = sessionmaker(bind=engine_test, expire_on_commit=False)


# Функция для запуска сервера
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


# Фикстура для базы данных
@pytest.fixture(autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


# Фикстура для замены зависимости get_db_session
@pytest.fixture
def override_get_db_session():
    def _override():
        with TestSession() as session:
            yield session
    app.dependency_overrides[get_db_session] = _override


# Фикстура для запуска FastAPI-сервера в отдельном процессе
@pytest.fixture(scope="module", autouse=True)
def start_server():
    process = Process(target=run_server, daemon=True)
    process.start()
    yield
    process.terminate()
    process.join()  # Убедиться, что процесс завершен



# Фикстура для асинхронного клиента
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        yield ac

