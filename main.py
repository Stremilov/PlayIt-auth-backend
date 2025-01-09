import asyncio
import uvicorn
import logging

from fastapi import FastAPI
from logging_loki import LokiHandler

from src.db.db import init_db
from src.api.routers import all_routers


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("auth_logger")

app = FastAPI(root_path="/playit/auth")

for router in all_routers:
    app.include_router(router)


async def main():
    logging.info("Инициализирую базу данных")
    init_db()

    logging.info("База данных инициализирована")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
