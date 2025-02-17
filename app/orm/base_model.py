from sqlalchemy import Integer, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.settings import settings


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.convention)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
