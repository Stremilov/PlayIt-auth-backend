from src.api.users import router as users_router
from src.api.sessions import router as sessions_router

all_routers = [
    users_router,
    sessions_router
]