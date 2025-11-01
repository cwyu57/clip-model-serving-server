from fastapi import FastAPI

from app.api import api_router
from app.core.exceptions import register_exception_handlers
from app.core.logger import get_logger, setup_logging
from app.middleware import add_process_time_header

# Setup logging before anything else
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="CLIP Model Serving Server",
    description="API for serving CLIP model",
    version="0.1.0",
    docs_url="/docs",
)

register_exception_handlers(app)

app.middleware("http")(add_process_time_header)

app.include_router(api_router)

logger.info("Application started successfully")
