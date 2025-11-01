from app.entity.repository.search_log import CreateSearchLogInputSchema
from app.entity.use_case.clip import SearchImageIn, SearchImageOut
from app.repository.search_log.search_log import SearchLogRepository
from app.service.clip.clip_service import CLIPService


class ImageSearchUseCase:
    def __init__(
        self,
        search_log_repository: SearchLogRepository,
        clip_service: CLIPService,
    ):
        self.search_log_repository = search_log_repository
        self.clip_service = clip_service
        # Hardcoded image URLs (as per requirement)
        self.image_urls = [
            "http://images.cocodataset.org/val2017/000000010363.jpg",
            "http://images.cocodataset.org/val2017/000000022192.jpg",
        ]

    async def search_image(self, search_image_in: SearchImageIn) -> SearchImageOut:
        # TODO: use all 328 images in the dataset provided
        # TODO: calculate image embeddings in advanced
        # TODO: save the text embeddings in the database along with the model info

        # Delegate to service layer for model operations
        most_similar_image_url = self.clip_service.find_most_similar_image(
            text=search_image_in.query,
            image_urls=self.image_urls,
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
