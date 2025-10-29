from io import BytesIO

import requests
import torch
from fastapi import APIRouter, status
from PIL import Image
from pydantic import BaseModel
from torch.nn.functional import cosine_similarity
from transformers import CLIPModel, CLIPProcessor

router = APIRouter()


class SearchRequestParams(BaseModel):
    query: str


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search for the most relevant image to the query",
    description="Search for the most relevant image to the query using the CLIP model",
)
async def search_image(request_params: SearchRequestParams) -> str:
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
    text = request_params.query

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
    cosine_scores = cosine_similarity(image_embeddings, text_embeddings)

    most_similar_index = int(torch.argmax(cosine_scores).item())
    most_similar_image_url = image_urls[most_similar_index]
    most_similar_image_similarity_score = (
        f"{cosine_scores[most_similar_index].item():.2f}"
    )

    return (
        f"The most relevant image to the query {text} is {most_similar_image_url} "
        f"with a similarity score of {most_similar_image_similarity_score}"
    )
