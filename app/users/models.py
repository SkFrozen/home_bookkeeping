from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.orm import BaseModel

if TYPE_CHECKING:
    from app.accounts import Account


class User(BaseModel):
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    groups: Mapped[list["Group"]] = relationship(
        back_populates="users", secondary="users_groups"
    )
    accounts: Mapped[list["Account"]] = relationship(back_populates="user")


class Group(BaseModel):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    note: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped[list["User"]] = relationship(
        back_populates="groups", secondary="users_groups"
    )
    accounts: Mapped[list["Account"]] = relationship(back_populates="group")


class UserGroup(BaseModel):
    __tablename__ = "users_groups"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "group_id",
        ),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
