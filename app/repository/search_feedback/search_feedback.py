from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.model.generated import SearchFeedbacks
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
