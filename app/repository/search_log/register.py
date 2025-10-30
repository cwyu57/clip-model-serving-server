from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repository.search_log.search_log import SearchLogRepository


def get_search_log_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SearchLogRepository:
    return SearchLogRepository(session)
