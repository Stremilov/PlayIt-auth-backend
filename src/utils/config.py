import os
from dotenv import load_dotenv

load_dotenv()

# Для создания БД
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_NAME = os.getenv("DATABASE_NAME", "postgres")
DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PORT = os.getenv("DATABASE_PORT", "5432")

SECRET_KEY = os.getenv("SECRET_KEY")  # Для fastapi-сессий в файле src/sessions/backend
