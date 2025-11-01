from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt  # type: ignore[import-untyped]

from app.core.config import get_current_config

# Get configuration
config = get_current_config()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
