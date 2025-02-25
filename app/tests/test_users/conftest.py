import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import User


@pytest.fixture
async def registered_user(session: AsyncSession):
    user = User(username="test", password="test")
    session.add(user)
    await session.commit()
