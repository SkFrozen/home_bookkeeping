from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(..., max_length=100)


class UserRegistrationSchema(UserSchema):
    password: str = Field(..., max_length=128)


class UserRegistrationResponseSchema(UserSchema):
    pass
