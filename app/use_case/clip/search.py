from app.entity.repository.search_log import CreateSearchLogInputSchema
from app.entity.use_case.clip import SearchImageIn, SearchImageOut
from app.repository.search_log.search_log import SearchLogRepository
from app.service.clip import CLIPService


class ImageSearchUseCase:
    def __init__(
        self,
        search_log_repository: SearchLogRepository,
        clip_service: CLIPService,
    ):
        self.search_log_repository = search_log_repository
        self.clip_service = clip_service

    async def search_image(self, search_image_in: SearchImageIn) -> SearchImageOut:
        # TODO: use all 328 images in the dataset provided
        # TODO: save the text embeddings in the database along with the model info
        # NOTE: Image embeddings are now precomputed and loaded from safetensors

        # Delegate to service layer for model operations
        most_similar_image_url = self.clip_service.find_most_similar_image(
            text=search_image_in.query,
        )

        # Focus on business logic: logging the search
        search_log = await self.search_log_repository.create_search_log(
            CreateSearchLogInputSchema(
                query=search_image_in.query,
                image_url=most_similar_image_url,
                user_id=search_image_in.user_id,
            )
        )

        return SearchImageOut(id=search_log.id, image_url=most_similar_image_url)
