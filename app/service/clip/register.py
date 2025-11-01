from app.service.clip.clip_service import CLIPService


def get_clip_service() -> CLIPService:
    return CLIPService()
