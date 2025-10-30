from typing import Annotated

from fastapi import Depends

from app.repository.search_log.register import get_search_log_repository
from app.repository.search_log.search_log import SearchLogRepository
from app.use_case.clip.clip import ClipUseCase


def get_clip_use_case(
    search_log_repository: Annotated[
        SearchLogRepository, Depends(get_search_log_repository)
    ],
) -> ClipUseCase:
    return ClipUseCase(search_log_repository)
