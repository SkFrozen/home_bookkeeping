from fastapi import APIRouter, Depends, HTTPException

from app.users.schemas import UserRegistrationResponseSchema, UserRegistrationSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/registration", response_model=UserRegistrationResponseSchema)
def registration_user_api_view(user_data: UserRegistrationSchema):
    pass
