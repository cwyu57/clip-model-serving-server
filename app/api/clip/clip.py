from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search for the most relevant image to the query",
    description="Search for the most relevant image to the query using the CLIP model",
)
async def search_image(query: str) -> str:
    return f"The most relevant image to the query {query} is ..."
