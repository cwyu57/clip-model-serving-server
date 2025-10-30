from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.model.generated import SearchFeedbacks
from app.entity.repository.search_feedback import UpsertSearchFeedbackInputSchema


class SearchFeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_search_feedback(
        self, input_schema: UpsertSearchFeedbackInputSchema
    ) -> SearchFeedbacks:
        """Upsert (insert or update) search feedback."""
        stmt = (
            insert(SearchFeedbacks)
            .values(
                search_log_id=input_schema.search_log_id,
                is_relevant=input_schema.is_relevant,
            )
            .on_conflict_do_update(
                index_elements=["search_log_id"],
                set_={
                    "is_relevant": input_schema.is_relevant,
                    "updated_at": func.now(),
                },
            )
            .returning(SearchFeedbacks)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
