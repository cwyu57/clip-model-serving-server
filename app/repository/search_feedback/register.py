from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repository.search_feedback.search_feedback import SearchFeedbackRepository


def get_search_feedback_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SearchFeedbackRepository:
    return SearchFeedbackRepository(session)
