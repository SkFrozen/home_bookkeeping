from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Account
from ..schemas import AccountCreationSchema, AccountUpdateSchema
from .exc import AccountNotFoundException


async def create_account(
    session: AsyncSession, user_id: int, account_data: AccountCreationSchema
) -> Account:
    account_dict = account_data.model_dump()
    account = await Account.create(session, user_id=user_id, **account_dict)
    return account


async def get_account(
    session: AsyncSession, user_id: int, account_name: str
) -> Account:
    account = await Account.get(session, user_id=user_id, name=account_name)
    if not account:
        raise AccountNotFoundException

    return account


async def get_all_user_accounts(session: AsyncSession, user_id: int) -> list[Account]:
    query = select(Account).where(Account.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def update_user_account(
    session: AsyncSession,
    user_id: int,
    account_name: str,
    account_data: AccountUpdateSchema,
):
    values = account_data.model_dump()
    query = (
        update(Account)
        .where(Account.name == account_name, Account.user_id == user_id)
        .values(**values)
        .returning(Account)
    )
    result = await session.execute(query)
    account = result.scalar()
    if not account:
        raise AccountNotFoundException

    await session.commit()
    return account


async def delete_user_account(
    session: AsyncSession, user_id: int, account_name: str
) -> None:
    account = await Account.get(session, user_id=user_id, name=account_name)
    if not account:
        raise AccountNotFoundException
    await account.delete(session)
