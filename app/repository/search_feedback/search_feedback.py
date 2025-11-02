import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.entity.model.generated import SearchFeedbacks, SearchLogs
from app.entity.repository.search_feedback import UpsertSearchFeedbackInputSchema


class SearchFeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_search_feedback(self, input_schema: UpsertSearchFeedbackInputSchema) -> SearchFeedbacks:
        """Insert search feedback."""
        feedback = SearchFeedbacks(
            search_log_id=input_schema.search_log_id,
            is_relevant=input_schema.is_relevant,
        )
        self.session.add(feedback)
        await self.session.flush()
        await self.session.refresh(feedback)
        return feedback

    async def get_user_feedback_with_search_logs(self, user_id: uuid.UUID) -> list[SearchFeedbacks]:
        """Get all feedback for a user with related search log data."""
        result = await self.session.execute(
            select(SearchFeedbacks)
            .join(SearchLogs, SearchFeedbacks.search_log_id == SearchLogs.id)
            .where(SearchLogs.user_id == user_id)
            .options(selectinload(SearchFeedbacks.search_log))
        )
        return list(result.scalars().all())
