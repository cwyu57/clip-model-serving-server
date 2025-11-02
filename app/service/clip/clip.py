import json
from pathlib import Path

import torch
from safetensors import safe_open
from transformers import CLIPModel, CLIPProcessor

from app.core.logger import get_logger

logger = get_logger(__name__)


class CLIPService:
    """Service for CLIP model operations.

    This service handles:
    - Model loading and caching
    - Precomputed image embeddings loading
    - Similarity computation

    Note:
        Do not instantiate this class directly. Use get_clip_service() instead
        to ensure the model is loaded only once and reused across all requests.
    """

    def __init__(self):
        """Initialize CLIP service and load model.

        Warning:
            This method loads the CLIP model which is resource-intensive.
            Always use get_clip_service() to get a singleton instance
            instead of creating new instances directly.
        """
        logger.info("Loading CLIP model...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        logger.info("CLIP model loaded successfully!")

        # Load precomputed image embeddings
        embeddings_path = Path("data/image_embeddings.safetensors")
        if not embeddings_path.exists():
            raise FileNotFoundError(
                f"Precomputed embeddings not found at {embeddings_path}. "
                "Please run scripts/precompute_image_embeddings.py first."
            )

        logger.info("Loading precomputed image embeddings...")
        with safe_open(str(embeddings_path), framework="pt") as f:
            self.precomputed_embeddings = f.get_tensor("embeddings")
            metadata = f.metadata()
            self.image_urls = json.loads(metadata["image_urls"])

        logger.info(f"Loaded {len(self.image_urls)} precomputed image embeddings")

    def compute_similarity_scores(self, text: str) -> tuple[torch.Tensor, list[str]]:
        """Compute similarity scores for all images given a text query.

        Uses precomputed image embeddings for faster inference.

        Args:
            text: Search query text

        Returns:
            Tuple of (cosine_scores, image_urls) where cosine_scores is a tensor
            of similarity scores for each image
        """
        # Process text only
        text_inputs = self.processor(text=text, return_tensors="pt", padding=True)

        # Generate text embeddings
        with torch.no_grad():
            text_features = self.model.get_text_features(**text_inputs)

        # Normalize text embeddings
        text_embeddings = text_features / text_features.norm(dim=-1, keepdim=True)

        # Compute cosine similarity with precomputed image embeddings
        cosine_scores = torch.cosine_similarity(self.precomputed_embeddings, text_embeddings)

        return cosine_scores, self.image_urls
