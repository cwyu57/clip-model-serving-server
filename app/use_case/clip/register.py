from typing import Annotated

from fastapi import Depends

from app.repository.search_feedback.register import get_search_feedback_repository
from app.repository.search_feedback.search_feedback import SearchFeedbackRepository
from app.repository.search_log.register import get_search_log_repository
from app.repository.search_log.search_log import SearchLogRepository
from app.use_case.clip.clip import ClipUseCase
from app.use_case.clip.feedback import FeedbackUseCase


def get_clip_use_case(
    search_log_repository: Annotated[
        SearchLogRepository, Depends(get_search_log_repository)
    ],
) -> ClipUseCase:
    return ClipUseCase(search_log_repository)


def get_feedback_use_case(
    search_feedback_repository: Annotated[
        SearchFeedbackRepository, Depends(get_search_feedback_repository)
    ],
    search_log_repository: Annotated[
        SearchLogRepository, Depends(get_search_log_repository)
    ],
) -> FeedbackUseCase:
    return FeedbackUseCase(search_feedback_repository, search_log_repository)
