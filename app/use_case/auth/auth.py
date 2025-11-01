from fastapi import HTTPException, status

from app.core.auth import create_access_token, verify_password
from app.entity.controller.auth import LoginResponse
from app.repository.user.user import UserRepository


class AuthUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def login(self, username: str, password: str) -> LoginResponse:
        """Authenticate user and return JWT access token."""
        # Get user from database
        user = await self.user_repository.get_user_by_username(username)

        # Check if user exists and password is correct
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        return LoginResponse(access_token=access_token, token_type="bearer")
