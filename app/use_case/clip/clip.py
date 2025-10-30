from io import BytesIO

import requests
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from app.entity.repository.search_log import CreateSearchLogInputSchema
from app.entity.use_case.clip import SearchImageIn, SearchImageOut
from app.repository.search_log.search_log import SearchLogRepository


class ClipUseCase:
    def __init__(self, search_log_repository: SearchLogRepository):
        self.search_log_repository = search_log_repository

    async def search_image(self, search_image_in: SearchImageIn) -> SearchImageOut:
        # Load pre-trained CLIP model and processor
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Load images
        image_urls = [
            "http://images.cocodataset.org/val2017/000000010363.jpg",
            "http://images.cocodataset.org/val2017/000000022192.jpg",
        ]
        images = [
            Image.open(BytesIO(requests.get(image_url).content)).convert("RGB")
            for image_url in image_urls
        ]

        # Prepare search term
        text = search_image_in.query

        # Preprocess inputs
        inputs = processor(text=text, images=images, return_tensors="pt", padding=True)

        # Generate embeddings
        with torch.no_grad():
            outputs = model(**inputs)

        # Extract and normalize image and text embeddings
        image_embeddings = outputs.image_embeds / outputs.image_embeds.norm(
            dim=-1, keepdim=True
        )
        text_embeddings = outputs.text_embeds / outputs.text_embeds.norm(
            dim=-1, keepdim=True
        )

        # Compute cosine similarity
        cosine_scores = torch.cosine_similarity(image_embeddings, text_embeddings)

        most_similar_index = int(torch.argmax(cosine_scores).item())
        most_similar_image_url = image_urls[most_similar_index]

        search_log = await self.search_log_repository.create_search_log(
            CreateSearchLogInputSchema(
                query=search_image_in.query, image_url=most_similar_image_url
            )
        )
        return SearchImageOut(id=search_log.id, image_url=most_similar_image_url)
