from fastapi import APIRouter

from .settings import settings
from .users import router as users_router

api_router = APIRouter(prefix=settings.api_prefix)

api_router.include_router(users_router)
