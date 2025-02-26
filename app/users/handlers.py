from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session

from .schemas import TokenPair, UserCredentialsSchema, UserRegistrationResponseSchema
from .services import create_jwt_token_pair, create_user, get_user_by_credentials

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRegistrationResponseSchema)
async def registration_user_handler(
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
