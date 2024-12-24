from uuid import UUID, uuid4
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from src.schemas.sessions import SessionData

cookie_params = CookieParameters(
    max_age=60 * 60 * 24 # время действия токена доступа 1 день
)

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE", #TODO убрать в .env
    cookie_params=cookie_params,
)

backend = InMemoryBackend[UUID, SessionData]()
