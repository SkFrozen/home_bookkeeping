from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session
from app.users import User
from app.users.services import get_current_user

from .models import Account
from .schemas import AccountCreationSchema, AccountResponseSchema
from .services import (
    AccountNotFoundException,
    create_account,
    get_account,
    get_all_user_accounts,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponseSchema)
async def create_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_data: AccountCreationSchema,
):

    return await create_account(session, user.id, account_data)


@router.get("{account_name}", response_model=AccountResponseSchema)
async def get_user_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_name: str,
):

    return await get_account(session, user.id, account_name)


@router.get("", response_model=list[AccountResponseSchema])
async def get_all_user_accounts_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    accounts = await get_all_user_accounts(session, user.id)
