import uuid

from pydantic import BaseModel


class UpsertSearchFeedbackInputSchema(BaseModel):
    search_log_id: uuid.UUID
    is_relevant: bool
