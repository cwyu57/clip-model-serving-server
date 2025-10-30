from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import create_access_token, verify_password
from app.entity.controller.auth import LoginResponse
from app.repository.user import UserRepository, get_user_repository

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User login (OAuth2 Password Flow)",
    description="Authenticate user and return JWT access token",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> LoginResponse:
    """Login endpoint for OAuth2 password flow - returns JWT token."""
    # Get user from database
    user = await user_repository.get_user_by_username(form_data.username)

    # Check if user exists and password is correct
    if user is None or not verify_password(form_data.password, user.hashed_password):
        # TODO: display error response in swagger UI
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(access_token=access_token, token_type="bearer")
