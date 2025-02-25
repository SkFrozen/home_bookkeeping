from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.operations import Expense, Income, Saving
from app.orm import BaseModel, CurrencyEnum, Manager

if TYPE_CHECKING:
    from app.users import Group, User


class Account(BaseModel, Manager):
    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND group_id IS NULL) OR (user_id IS NULL AND group_id IS NOT NULL)",
            "account_owner",
        ),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[int] = mapped_column(default=0)
    currency: Mapped[CurrencyEnum] = mapped_column(
        PgEnum(CurrencyEnum),
        nullable=False,
        default=CurrencyEnum.RUB,
    )
    note: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="accounts")
    group: Mapped["Group"] = relationship(back_populates="accounts")
    incomes: Mapped["Income"] = relationship(back_populates="account")
    savings: Mapped["Saving"] = relationship(back_populates="account")
    expenses: Mapped["Expense"] = relationship(back_populates="account")
