import uuid

from pydantic import BaseModel


class SearchRequestParams(BaseModel):
    query: str


class SearchRequestResponse(BaseModel):
    id: uuid.UUID
    image_url: str
