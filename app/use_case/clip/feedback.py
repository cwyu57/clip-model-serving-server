from app.entity.repository.search_feedback import UpsertSearchFeedbackInputSchema
from app.entity.use_case.clip import UpsertFeedbackIn, UpsertFeedbackOut
from app.repository.search_feedback.search_feedback import SearchFeedbackRepository


class FeedbackUseCase:
    def __init__(self, search_feedback_repository: SearchFeedbackRepository):
        self.search_feedback_repository = search_feedback_repository

    async def upsert_feedback(
        self, upsert_feedback_in: UpsertFeedbackIn
    ) -> UpsertFeedbackOut:
        """Upsert (insert or update) search feedback."""
        feedback = await self.search_feedback_repository.upsert_search_feedback(
            UpsertSearchFeedbackInputSchema(
                search_log_id=upsert_feedback_in.search_log_id,
                is_relevant=upsert_feedback_in.is_relevant,
            )
        )
        return UpsertFeedbackOut(
            id=feedback.id,
            search_log_id=feedback.search_log_id,
            is_relevant=feedback.is_relevant,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )
