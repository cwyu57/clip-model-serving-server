from app.entity.repository.search_log import CreateSearchLogInputSchema
from app.entity.use_case.clip import SearchImageIn, SearchImageOut
from app.repository.search_feedback.search_feedback import SearchFeedbackRepository
from app.repository.search_log.search_log import SearchLogRepository
from app.service.clip import CLIPService
from app.service.reranking import RerankingService


class ImageSearchUseCase:
    def __init__(
        self,
        search_log_repository: SearchLogRepository,
        search_feedback_repository: SearchFeedbackRepository,
        clip_service: CLIPService,
        reranking_service: RerankingService,
    ):
        self.search_log_repository = search_log_repository
        self.search_feedback_repository = search_feedback_repository
        self.clip_service = clip_service
        self.reranking_service = reranking_service

    async def search_image(self, search_image_in: SearchImageIn) -> SearchImageOut:
        # Get similarity scores from CLIP model
        cosine_scores, image_urls = self.clip_service.compute_similarity_scores(text=search_image_in.query)

        # Query user feedback
        user_feedbacks = await self.search_feedback_repository.get_user_feedback_with_search_logs(
            user_id=search_image_in.user_id
        )

        # Rerank with feedback if available
        most_similar_image_url = self.reranking_service.rerank_with_feedback(
            cosine_scores=cosine_scores,
            image_urls=image_urls,
            current_query=search_image_in.query,
            user_feedbacks=user_feedbacks,
        )

        # logging the search log
        search_log = await self.search_log_repository.create_search_log(
            CreateSearchLogInputSchema(
                query=search_image_in.query,
                image_url=most_similar_image_url,
                user_id=search_image_in.user_id,
            )
        )

        return SearchImageOut(id=search_log.id, image_url=most_similar_image_url)
