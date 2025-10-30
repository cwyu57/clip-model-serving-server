from fastapi._compat.v1 import BaseModel


class CreateSearchLogInputSchema(BaseModel):
    query: str
    image_url: str
