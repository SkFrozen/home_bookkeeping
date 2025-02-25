from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY

headers = {"WWW-Authenticate": "Bearer"}

CredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers=headers,
)
InvalidRefreshTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
    headers=headers,
)
InvalidAccessTokenException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
    headers=headers,
)
UserAlreadyExistException = HTTPException(
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    detail="User already exist",
)
