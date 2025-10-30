import uuid

from pydantic import BaseModel


class CreateSearchLogInputSchema(BaseModel):
    query: str
    image_url: str
    user_id: uuid.UUID
