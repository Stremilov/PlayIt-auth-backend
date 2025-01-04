import asyncio
import uvicorn
import logging

from fastapi import FastAPI

from src.db.db import init_db
from src.api.routers import all_routers

# Логирую только уровень error+ (error, critical)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app_logger")

app = FastAPI(root_path="/playit/auth")

for router in all_routers:
    app.include_router(router)


async def main():
    logging.info("Starting init_db()")
    init_db()
    logging.info("Starting FastAPI app")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
