from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session

from ..models import User
from ..schemas import UserCredentialsSchema
from .exc import CredentialsException, UserAlreadyExistException
from .jwt import USER_IDENTIFIER, _get_token_payload, oauth2_scheme
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


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    payload = _get_token_payload(token, "access")
    user = await User.get(session, id=payload[USER_IDENTIFIER])
    if not user:
        raise CredentialsException

    return user
