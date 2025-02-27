from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session

from .schemas import (
    AccessToken,
    RefreshToken,
    TokenPair,
    UserCredentialsSchema,
    UserRegistrationResponseSchema,
)
from .services import (
    create_jwt_token_pair,
    create_user,
    get_user_by_credentials,
    refresh_access_token,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRegistrationResponseSchema)
async def register_user_handler(
    user_data: UserCredentialsSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
):

    return await create_user(session, user_data)


@router.post("/token", response_model=TokenPair)
async def get_token_pair_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_data: UserCredentialsSchema,
):
    user = await get_user_by_credentials(session, user_data)
    return create_jwt_token_pair(user_id=user.id)


@router.post("/token/refresh", response_model=AccessToken)
def refresh_token_handler(token: RefreshToken):
    access_token = refresh_access_token(token.refresh_token)
    return AccessToken(access_token=access_token)
