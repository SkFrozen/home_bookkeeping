from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.settings import settings

from ..schemas import TokenPair
from .exc import (
    CredentialsException,
    InvalidAccessTokenException,
    InvalidRefreshTokenException,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/users/token")
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS512"
USER_IDENTIFIER = "user_id"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_HOURS = settings.refresh_token_expire_hours


def create_jwt_token_pair(user_id: int) -> TokenPair:
    access_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "refresh"},
        timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS),
    )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


def refresh_access_token(refresh_token: str) -> str:
    payload = _get_token_payload(refresh_token, "refresh")

    return _create_jwt_token(
        {USER_IDENTIFIER: payload[USER_IDENTIFIER], "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def _create_jwt_token(payload: dict, delta: datetime) -> str:
    expires_delta = datetime.now(UTC) + delta
    payload.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _get_token_payload(token: str, token_type: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (JWTError, ExpiredSignatureError):
        raise _get_invalid_token_exc(token_type)

    if payload.get("type") != token_type:
        raise _get_invalid_token_exc(token_type)
    if payload.get(USER_IDENTIFIER) is None:
        raise CredentialsException

    return payload


def _get_invalid_token_exc(token_type: str) -> HTTPException:
    if token_type == "access":
        return InvalidAccessTokenException

    return InvalidRefreshTokenException
