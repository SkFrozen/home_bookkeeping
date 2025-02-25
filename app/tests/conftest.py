from typing import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.orm import get_session
from app.settings import settings
from main import main_app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    assert settings.mode == "TEST"
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest.fixture(name="session")
async def async_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(url=settings.get_db_url)
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest.fixture(name="client")
async def async_client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def get_session_override() -> AsyncIterator[AsyncSession]:
        yield session

    main_app.dependency_overrides[get_session] = get_session_override

    transport = ASGITransport(app=main_app)
    async with AsyncClient(
        transport=transport, base_url=f"http://test:{settings.api_prefix}"
    ) as client:
        yield client
        main_app.dependency_overrides.clear()
