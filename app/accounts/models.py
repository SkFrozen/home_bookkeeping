from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.orm import BaseModel, CurrencyEnum, OwnerTypeEnum

if TYPE_CHECKING:
    from app.users import Group, User


class Account(BaseModel):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[int] = mapped_column(default=0)
    currency: Mapped[CurrencyEnum]
    note: Mapped[str | None]
    owner_type: Mapped[OwnerTypeEnum]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    owner_id: Mapped[int] = mapped_column()

    user: Mapped["User"] = relationship(
        back_populates="accounts",
        foreign_keys=[owner_id],
        primaryjoin="and_(Account.owner_id == User.id, Account.owner_type == 'user')",
        overlaps="group",
    )
    group: Mapped["Group"] = relationship(
        back_populates="accounts",
        foreign_keys=[owner_id],
        primaryjoin="and_(Account.owner_id == Group.id, Account.owner_type == 'group')",
        overlaps="user",
    )
