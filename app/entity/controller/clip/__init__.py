import datetime
import uuid

from pydantic import BaseModel


class SearchRequestParams(BaseModel):
    query: str


class SearchRequestResponse(BaseModel):
    id: uuid.UUID
    image_url: str


class FeedbackRequestParams(BaseModel):
    is_relevant: bool


class FeedbackResponse(BaseModel):
    id: uuid.UUID
    search_log_id: uuid.UUID
    is_relevant: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
