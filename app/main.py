from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.exceptions import register_exception_handlers
from app.core.logger import get_logger, setup_logging
from app.middleware import add_process_time_header
from app.service.clip import get_clip_service

# Setup logging before anything else
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events.

    Startup:
        - Initialize CLIP service and preload model
        - Load precomputed embeddings

    Shutdown:
        - Perform cleanup if needed
    """
    # Startup
    logger.info("Initializing CLIP service...")
    get_clip_service()  # Force initialization on startup
    logger.info("CLIP service initialized successfully!")

    yield  # Application is running

    # Shutdown
    logger.info("Application shutting down...")


app = FastAPI(
    title="CLIP Model Serving Server",
    description="API for serving CLIP model",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.middleware("http")(add_process_time_header)

app.include_router(api_router)

logger.info("Application started successfully")
