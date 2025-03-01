from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import get_session
from app.users import User
from app.users.services import get_current_user

from .schemas import (
    AccountCreationSchema,
    AccountDeleteSchema,
    AccountResponseSchema,
    AccountUpdateSchema,
)
from .services import (
    create_account,
    delete_user_account,
    get_account,
    get_all_user_accounts,
    update_user_account,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponseSchema)
async def create_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_data: AccountCreationSchema,
):

    return await create_account(session, user.id, account_data)


@router.get("", response_model=AccountResponseSchema)
async def get_user_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_name: str,
):

    return await get_account(session, user.id, account_name)


@router.get("/my_accounts", response_model=list[AccountResponseSchema | None])
async def get_all_user_accounts_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    accounts = await get_all_user_accounts(session, user.id)

    return accounts


@router.put("", response_model=AccountResponseSchema)
async def update_user_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_name: str,
    account_data: AccountUpdateSchema,
):
    account = await update_user_account(session, user.id, account_name, account_data)
    return account


@router.delete("", response_model=AccountDeleteSchema)
async def delete_user_account_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    account_name: str,
):
    await delete_user_account(session, user.id, account_name)
    return AccountDeleteSchema(message=f"The account {account_name} has been deleted")
