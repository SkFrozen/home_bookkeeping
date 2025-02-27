from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app import api_router
from app.orm import db_helper
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_helper.init(url=settings.get_db_url, echo=True)
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.host, port=settings.port, reload=True)
