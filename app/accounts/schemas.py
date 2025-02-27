from datetime import datetime

from pydantic import Field

from app.base_schema import CustomeBaseSchema
from app.orm import CurrencyEnum


class AccountCreationSchema(CustomeBaseSchema):
    name: str
    balance: int
    currency: CurrencyEnum = Field(default=...)
    note: str | None


class AccountResponseSchema(AccountCreationSchema):
    created_at: datetime
