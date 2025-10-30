from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.entity.controller.clip import SearchRequestParams, SearchRequestResponse
from app.entity.use_case.clip import SearchImageIn
from app.use_case.clip import ClipUseCase, get_clip_use_case

router = APIRouter()


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search for the most relevant image to the query",
    description="Search for the most relevant image to the query using the CLIP model",
)
async def search_image(
    request_params: SearchRequestParams,
    clip_use_case: Annotated[ClipUseCase, Depends(get_clip_use_case)],
) -> SearchRequestResponse:
    result = await clip_use_case.search_image(SearchImageIn(query=request_params.query))
    return SearchRequestResponse(id=result.id, image_url=result.image_url)
