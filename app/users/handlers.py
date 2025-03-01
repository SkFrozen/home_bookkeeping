from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session

from .models import User
from .schemas import (
    AccessToken,
    GroupSchema,
    RefreshToken,
    TokenPair,
    UserCredentialsSchema,
    UserRegistrationResponseSchema,
)
from .services import (
    create_group,
    create_jwt_token_pair,
    create_user,
    exit_from_group,
    get_current_user,
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


@router.post("/groups", response_model=GroupSchema)
async def create_group_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    group_data: GroupSchema,
):
    return await create_group(session, user, group_data)


@router.get("/groups", response_model=dict[str, str])
async def exit_from_group_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    group_name: str,
):

    await exit_from_group(session, user, group_name)
    return {"message": f"You are exit from group {group_name}"}
