import uuid

from pydantic import BaseModel


class SearchImageIn(BaseModel):
    query: str


class SearchImageOut(BaseModel):
    id: uuid.UUID
    image_url: str
