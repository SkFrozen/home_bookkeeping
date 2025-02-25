from datetime import datetime

from pydantic import BaseModel, Field


class UserCredentialsSchema(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=128)


class UserRegistrationResponseSchema(BaseModel):
    id: int
    username: str = Field(..., max_length=100)
    created_at: datetime


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class Refreshtoken(BaseModel):
    refresh_token: str
