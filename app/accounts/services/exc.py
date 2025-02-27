from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

AccountNotFoundException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Account not found",
)
