from uuid import uuid4

from src.schemas.sessions import SessionData
from src.sessions.backend import backend, cookie


async def login(response, name):
    session = uuid4()
    data = SessionData(username=name)
    await backend.create(session, data)
    cookie.attach_to_response(response, session)

