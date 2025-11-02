import torch
from transformers import CLIPModel, CLIPProcessor

from app.core.logger import get_logger
from app.entity.model.generated import SearchFeedbacks

logger = get_logger(__name__)


class RerankingService:
    """Service for reranking search results based on user feedback.

    This service handles:
    - Computing query similarity using CLIP text embeddings
    - Adjusting image scores based on user feedback
    """

    def __init__(self, clip_model: CLIPModel, clip_processor: CLIPProcessor):
        """Initialize reranking service with CLIP model components.

        Args:
            clip_model: The CLIP model for computing text embeddings
            clip_processor: The CLIP processor for text preprocessing
        """
        self.model = clip_model
        self.processor = clip_processor

    def compute_query_similarity(self, query1: str, query2: str) -> float:
        """Compute cosine similarity between two text queries.

        Args:
            query1: First query text
            query2: Second query text

        Returns:
            Cosine similarity score between 0 and 1
        """
        # Process both texts
        text_inputs = self.processor(text=[query1, query2], return_tensors="pt", padding=True)

        # Generate text embeddings
        with torch.no_grad():
            text_features = self.model.get_text_features(**text_inputs)

        # Normalize embeddings
        text_embeddings = text_features / text_features.norm(dim=-1, keepdim=True)

        # Compute cosine similarity
        similarity = torch.cosine_similarity(text_embeddings[0:1], text_embeddings[1:2])
        return float(similarity.item())

    def rerank_with_feedback(
        self,
        cosine_scores: torch.Tensor,
        image_urls: list[str],
        current_query: str,
        user_feedbacks: list[SearchFeedbacks],
        similarity_threshold: float = 0.7,
        feedback_weight: float = 0.2,
    ) -> str:
        """Rerank images based on user feedback.

        Args:
            cosine_scores: Original cosine similarity scores from CLIP
            image_urls: List of image URLs corresponding to scores
            current_query: Current search query
            user_feedbacks: User's historical feedback with search logs
            similarity_threshold: Minimum query similarity to consider feedback (default: 0.7)
            feedback_weight: Weight for feedback adjustment (default: 0.2)

        Returns:
            URL of the best image after reranking
        """
        # If no feedback, return image with highest original score
        if not user_feedbacks:
            most_similar_index = int(torch.argmax(cosine_scores).item())
            return image_urls[most_similar_index]

        # Build feedback adjustments per image URL
        feedback_adjustments = {}

        for feedback in user_feedbacks:
            # Get query from related search log
            feedback_query = feedback.search_log.query
            feedback_image_url = feedback.search_log.image_url

            # Compute query similarity
            query_similarity = self.compute_query_similarity(current_query, feedback_query)

            # Only consider feedback if queries are similar enough
            if query_similarity < similarity_threshold:
                continue

            # Initialize feedback counts for this image
            if feedback_image_url not in feedback_adjustments:
                feedback_adjustments[feedback_image_url] = {"positive": 0, "negative": 0}

            # Count positive/negative feedback
            if feedback.is_relevant:
                feedback_adjustments[feedback_image_url]["positive"] += 1
            else:
                feedback_adjustments[feedback_image_url]["negative"] += 1

        # Adjust scores based on feedback
        adjusted_scores = cosine_scores.clone()

        for idx, image_url in enumerate(image_urls):
            if image_url in feedback_adjustments:
                counts = feedback_adjustments[image_url]
                positive = counts["positive"]
                negative = counts["negative"]
                total = positive + negative

                if total > 0:
                    # Adjust score: original_score * (1 + feedback_weight * (positive - negative) / total)
                    net_feedback = (positive - negative) / total
                    adjustment_factor = 1 + feedback_weight * net_feedback
                    adjusted_scores[idx] = adjusted_scores[idx] * adjustment_factor

                    logger.debug(
                        f"Adjusted score for {image_url}: "
                        f"positive={positive}, negative={negative}, "
                        f"adjustment_factor={adjustment_factor:.3f}"
                    )

        # Find best image after adjustment
        most_similar_index = int(torch.argmax(adjusted_scores).item())
        return image_urls[most_similar_index]
