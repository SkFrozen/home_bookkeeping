from datetime import datetime

from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.orm.base_model import BaseModel


class User(BaseModel):
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    groups: Mapped[list["Group"]] = relationship(
        back_populates="users", lazy="joined", secondary="users_groups"
    )


class Group(BaseModel):
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped[list["User"]] = relationship(
        back_populates="groups", secondary="users_groups"
    )


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
