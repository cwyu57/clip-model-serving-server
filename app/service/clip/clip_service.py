from io import BytesIO

import requests
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class CLIPService:
    """Service for CLIP model operations.

    This service handles:
    - Model loading and caching
    - Image processing
    - Similarity computation
    """

    def __init__(self):
        """Initialize CLIP service and load model."""
        print("Loading CLIP model...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        print("CLIP model loaded successfully!")

    def find_most_similar_image(self, text: str, image_urls: list[str]) -> str:
        """Find the most similar image to the given text query.

        Args:
            text: Search query text
            image_urls: List of image URLs to search through

        Returns:
            URL of the most similar image
        """
        # Load images
        images = [Image.open(BytesIO(requests.get(url).content)).convert("RGB") for url in image_urls]

        # Preprocess inputs
        inputs = self.processor(text=text, images=images, return_tensors="pt", padding=True)

        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract and normalize embeddings
        image_embeddings = outputs.image_embeds / outputs.image_embeds.norm(dim=-1, keepdim=True)
        text_embeddings = outputs.text_embeds / outputs.text_embeds.norm(dim=-1, keepdim=True)

        # Compute cosine similarity
        cosine_scores = torch.cosine_similarity(image_embeddings, text_embeddings)

        # Find most similar
        most_similar_index = int(torch.argmax(cosine_scores).item())
        return image_urls[most_similar_index]
