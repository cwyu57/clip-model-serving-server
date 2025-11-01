from typing import Annotated

from fastapi import Depends

from app.repository.search_feedback import SearchFeedbackRepository, get_search_feedback_repository
from app.repository.search_log import SearchLogRepository, get_search_log_repository
from app.use_case.clip.feedback import FeedbackUseCase
from app.use_case.clip.search import ImageSearchUseCase


def get_image_search_use_case(
    search_log_repository: Annotated[SearchLogRepository, Depends(get_search_log_repository)],
) -> ImageSearchUseCase:
    return ImageSearchUseCase(search_log_repository)


def get_feedback_use_case(
    search_feedback_repository: Annotated[SearchFeedbackRepository, Depends(get_search_feedback_repository)],
    search_log_repository: Annotated[SearchLogRepository, Depends(get_search_log_repository)],
) -> FeedbackUseCase:
    return FeedbackUseCase(search_feedback_repository, search_log_repository)
