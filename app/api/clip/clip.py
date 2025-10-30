import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.entity.controller.clip import (
    FeedbackRequestParams,
    FeedbackResponse,
    SearchRequestParams,
    SearchRequestResponse,
)
from app.entity.model.generated import Users
from app.entity.use_case.clip import SearchImageIn, UpsertFeedbackIn
from app.use_case.clip import (
    ClipUseCase,
    FeedbackUseCase,
    get_clip_use_case,
    get_feedback_use_case,
)

router = APIRouter()


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search for the most relevant image to the query",
    description="Search for the most relevant image to the query using the CLIP model",
)
async def search_image(
    request_params: SearchRequestParams,
    current_user: Annotated[Users, Depends(get_current_user)],
    clip_use_case: Annotated[ClipUseCase, Depends(get_clip_use_case)],
) -> SearchRequestResponse:
    result = await clip_use_case.search_image(
        SearchImageIn(query=request_params.query, user_id=current_user.id)
    )
    return SearchRequestResponse(id=result.id, image_url=result.image_url)


@router.put(
    "/search/{search_id}/feedback",
    status_code=status.HTTP_200_OK,
    summary="Submit feedback for a search result",
    description=(
        "Create or update feedback for a search result indicating if it was relevant"
    ),
)
async def upsert_search_feedback(
    search_id: uuid.UUID,
    request_params: FeedbackRequestParams,
    current_user: Annotated[Users, Depends(get_current_user)],
    feedback_use_case: Annotated[FeedbackUseCase, Depends(get_feedback_use_case)],
) -> FeedbackResponse:
    result = await feedback_use_case.upsert_feedback(
        UpsertFeedbackIn(
            search_log_id=search_id,
            is_relevant=request_params.is_relevant,
            user_id=current_user.id,
        )
    )
    return FeedbackResponse(
        id=result.id,
        search_log_id=result.search_log_id,
        is_relevant=result.is_relevant,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
