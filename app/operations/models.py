from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.orm import BaseModel, ExpenseCategoryEnum, IncomeCategoryEnum

if TYPE_CHECKING:
    from app.accounts import Account


class Income(BaseModel):
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[IncomeCategoryEnum]
    note: Mapped[str | None]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="incomes")


class Expense(BaseModel):
    amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[ExpenseCategoryEnum]
    note: Mapped[str | None]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="expenses")


class Saving(BaseModel):
    target_amount: Mapped[int]
    current_amount: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    category: Mapped[ExpenseCategoryEnum]
    periodicity: Mapped[str | None]
    note: Mapped[str]

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )

    account: Mapped["Account"] = relationship(back_populates="savings")
