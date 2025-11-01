import os


class BaseConfig:
    """Base configuration class that reads from environment variables."""

    # JWT Configuration
    JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str | None = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

    # Database Configuration
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str | None = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str | None = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str | None = os.getenv("POSTGRES_PORT")

    # Database Options
    ENABLE_SQL_ECHO: bool = os.getenv("ENABLE_SQL_ECHO", "false").lower() == "true"

    # Application Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def get_database_url(cls) -> str:
        """Build and return the database URL.

        Note: This method assumes validate() has been called.
        """
        return (
            f"postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@"
            f"{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        )

    @classmethod
    def validate(cls) -> None:
        """Validate that all required configuration values are set."""
        errors = []

        # JWT validation
        if not cls.JWT_SECRET_KEY:
            errors.append("JWT_SECRET_KEY is required")
        if not cls.JWT_ALGORITHM:
            errors.append("JWT_ALGORITHM is required")

        # Database validation
        if not cls.POSTGRES_USER:
            errors.append("POSTGRES_USER is required")
        if not cls.POSTGRES_PASSWORD:
            errors.append("POSTGRES_PASSWORD is required")
        if not cls.POSTGRES_DB:
            errors.append("POSTGRES_DB is required")
        if not cls.POSTGRES_HOST:
            errors.append("POSTGRES_HOST is required")
        if not cls.POSTGRES_PORT:
            errors.append("POSTGRES_PORT is required")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
