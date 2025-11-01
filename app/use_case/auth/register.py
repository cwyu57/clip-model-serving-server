from typing import Annotated

from fastapi import Depends

from app.repository.user import UserRepository, get_user_repository
from app.use_case.auth.auth import AuthUseCase


def get_auth_use_case(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthUseCase:
    return AuthUseCase(user_repository)
