from fastapi import APIRouter

from app.accounts import router as accounts_router
from app.users import router as users_router

from .settings import settings

api_router = APIRouter(prefix=settings.api_prefix)

api_router.include_router(users_router)
api_router.include_router(accounts_router)
