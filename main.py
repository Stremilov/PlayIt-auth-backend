import asyncio
import uvicorn
import logging

from fastapi import FastAPI
from logging_loki import LokiHandler

from src.db.db import init_db
from src.api.routers import all_routers

LOKI_URL = "http://loki:3100/loki/api/v1/push"
LOKI_TAGS = {"application": "playit-auth"}

loki_handler = LokiHandler(
    url=LOKI_URL,
    tags=LOKI_TAGS,
    version="1",
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app_logger")
logger.addHandler(loki_handler)
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
