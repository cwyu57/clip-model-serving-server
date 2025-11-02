from functools import lru_cache

from app.core.logger import get_logger
from app.service.clip import get_clip_service
from app.service.reranking import RerankingService

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_reranking_service() -> RerankingService:
    """Get or create the singleton RerankingService instance.

    This function ensures only one RerankingService instance exists,
    which is important because it reuses the CLIP model from CLIPService.

    Returns:
        The singleton RerankingService instance

    Note:
        Always use this function instead of instantiating RerankingService directly.
    """

    clip_service = get_clip_service()

    logger.info("Creating RerankingService with shared CLIP model...")

    return RerankingService(clip_model=clip_service.model, clip_processor=clip_service.processor)
