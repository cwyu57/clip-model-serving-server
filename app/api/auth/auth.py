from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.entity.controller.auth import LoginResponse
from app.use_case.auth import AuthUseCase, get_auth_use_case

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User login (OAuth2 Password Flow)",
    description="Authenticate user and return JWT access token",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
) -> LoginResponse:
    """Login endpoint for OAuth2 password flow - returns JWT token."""
    return await auth_use_case.login(form_data.username, form_data.password)
