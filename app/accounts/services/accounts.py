from sqlalchemy.ext.asyncio import AsyncSession

from app.accounts.schemas import AccountCreationSchema

from ..models import Account
from .exc import AccountNotFoundException


async def create_account(
    session: AsyncSession, user_id: int, account_data: AccountCreationSchema
):
    account_dict = account_data.model_dump()
    account = await Account.create(session, user_id=user_id, **account_dict)
    return account


async def get_account(session: AsyncSession, user_id: int, account_name: str):
    account = await Account.get(session, user_id=user_id, name=account_name)
    if not account:
        raise AccountNotFoundException

    return account


async def get_all_user_accounts(session, user_id):
    pass
