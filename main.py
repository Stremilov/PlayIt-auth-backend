import asyncio
import uvicorn
import logging

from fastapi import FastAPI, WebSocket
# from logging_loki import LokiHandler

from src.db.db import init_db
from src.api.routers import all_routers

from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("auth_logger")

app = FastAPI(root_path="/playit/auth")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")


for router in all_routers:
    app.include_router(router)


async def main():
    logging.info("Инициализирую базу данных")
    init_db()

    logging.info("База данных инициализирована")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
