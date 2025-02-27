import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import UserCredentialsSchema
from app.users.services import create_user


@pytest.fixture
async def registered_user(session: AsyncSession):
    await create_user(session, UserCredentialsSchema(username="test", password="test"))
