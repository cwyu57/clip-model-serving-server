from fastapi import HTTPException, status

from app.entity.repository.search_feedback import UpsertSearchFeedbackInputSchema
from app.entity.use_case.clip import UpsertFeedbackIn, UpsertFeedbackOut
from app.repository.search_feedback.search_feedback import SearchFeedbackRepository
from app.repository.search_log.search_log import SearchLogRepository


class FeedbackUseCase:
    def __init__(
        self,
        search_feedback_repository: SearchFeedbackRepository,
        search_log_repository: SearchLogRepository,
    ):
        self.search_feedback_repository = search_feedback_repository
        self.search_log_repository = search_log_repository

    async def create_feedback(self, upsert_feedback_in: UpsertFeedbackIn) -> UpsertFeedbackOut:
        """Create search feedback."""

        search_log = await self.search_log_repository.get_search_log_by_id(upsert_feedback_in.search_log_id)
        if search_log is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Search log not found",
            )
        if upsert_feedback_in.user_id != search_log.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to create feedback for this search log",
            )

        feedback = await self.search_feedback_repository.insert_search_feedback(
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
