from functools import lru_cache

from app.service.clip.clip import CLIPService


@lru_cache(maxsize=1)
def get_clip_service() -> CLIPService:
    """Get or create a singleton instance of CLIPService.

    The model is loaded only once and reused across all requests.
    This significantly improves performance by avoiding repeated model loading.
    """
    return CLIPService()
