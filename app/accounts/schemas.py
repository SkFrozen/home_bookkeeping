from datetime import datetime

from pydantic import BaseModel, Field

from app.base_schema import CustomeBaseSchema
from app.orm import CurrencyEnum


class AccountCreationSchema(CustomeBaseSchema):
    name: str
    balance: int
    currency: CurrencyEnum
    note: str | None = Field(default=None)


class AccountResponseSchema(AccountCreationSchema):
    created_at: datetime


class AccountUpdateSchema(AccountCreationSchema):
    pass


class AccountDeleteSchema(BaseModel):
    message: str
