from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class SearchRequestParams(BaseModel):
    query: str


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search for the most relevant image to the query",
    description="Search for the most relevant image to the query using the CLIP model",
)
async def search_image(request_params: SearchRequestParams) -> str:
    return f"The most relevant image to the query {request_params.query} is ..."
