from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..schemas import UserCredentialsSchema
from .exc import CredentialsException, UserAlreadyExistException
from .utils import get_password_hash, verify_password


async def create_user(session: AsyncSession, user_data: UserCredentialsSchema) -> User:
    if await User.exists(session, username=user_data.username):
        raise UserAlreadyExistException

    encrypted_password = get_password_hash(user_data.password)
    user = await User.create(
        session, username=user_data.username, password=encrypted_password
    )

    return user


async def get_user_by_credentials(
    session: AsyncSession, user_data: UserCredentialsSchema
) -> User:
    user = await User.get(session, username=user_data.username)
    if not user or not verify_password(user_data.password, user.password):
        raise CredentialsException

    return user
