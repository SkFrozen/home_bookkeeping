from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from app.settings import settings
from app.orm import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.host, port=settings.port, reload=True)
