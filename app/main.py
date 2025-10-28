from fastapi import FastAPI

from app.api import api_router

app = FastAPI(
    title="CLIP Model Serving Server",
    description="API for serving CLIP model",
    version="0.1.0",
    docs_url="/docs",
)

app.include_router(api_router)
