from datetime import datetime

from pydantic import Field

from app.base_schema import CustomeBaseSchema


class UserCredentialsSchema(CustomeBaseSchema):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=128)


class UserRegistrationResponseSchema(CustomeBaseSchema):
    id: int
    username: str = Field(..., max_length=100)
    created_at: datetime


class TokenPair(CustomeBaseSchema):
    access_token: str
    refresh_token: str


class AccessToken(CustomeBaseSchema):
    access_token: str


class RefreshToken(CustomeBaseSchema):
    refresh_token: str
