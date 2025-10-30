import datetime
import uuid

from pydantic import BaseModel


class SearchImageIn(BaseModel):
    query: str


class SearchImageOut(BaseModel):
    id: uuid.UUID
    image_url: str


class UpsertFeedbackIn(BaseModel):
    search_log_id: uuid.UUID
    is_relevant: bool


class UpsertFeedbackOut(BaseModel):
    id: uuid.UUID
    search_log_id: uuid.UUID
    is_relevant: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
