from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.orm import BaseModel, ExpenseCategoryEnum, IncomeCategoryEnum, Manager

if TYPE_CHECKING:
    from app.accounts import Account


class Income(BaseModel, Manager):
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[IncomeCategoryEnum] = mapped_column(
        PgEnum(IncomeCategoryEnum),
        nullable=False,
        default=IncomeCategoryEnum.salary,
    )
    note: Mapped[str | None]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="incomes")


class Expense(BaseModel, Manager):
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[ExpenseCategoryEnum] = mapped_column(
        PgEnum(ExpenseCategoryEnum),
        nullable=False,
        default=ExpenseCategoryEnum.regular_payments,
    )
    note: Mapped[str | None]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="expenses")


class Saving(BaseModel):
    target_amount: Mapped[int]
    current_amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[ExpenseCategoryEnum] = mapped_column(
        PgEnum(ExpenseCategoryEnum),
        nullable=False,
        default=ExpenseCategoryEnum.car,
    )
    periodicity: Mapped[str | None]
    note: Mapped[str]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="savings")
