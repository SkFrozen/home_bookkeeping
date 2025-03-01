from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Group, User
from ..schemas import GroupSchema
from .exc import GroupNotFoundException


async def create_group(
    session: AsyncSession, user: User, group_data: GroupSchema
) -> Group:
    values = group_data.model_dump()
    group = Group(**values)
    groups = await user.awaitable_attrs.groups
    groups.append(group)
    session.add(user)
    await session.commit()
    return group


async def exit_from_group(session: AsyncSession, user: User, group_name: str):
    groups = await user.awaitable_attrs.groups
    group = list(filter(lambda group: group.name == group_name, groups))
    if not group:
        raise GroupNotFoundException
    groups.remove(group)
    await session.commit()
