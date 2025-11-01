import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_current_config

# Configure logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Get current configuration
config = get_current_config()

# Build DATABASE_URL from configuration
DATABASE_URL = config.get_database_url()

# Enable SQL logging
ENABLE_SQL_ECHO = config.ENABLE_SQL_ECHO

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=ENABLE_SQL_ECHO)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
