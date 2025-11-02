"""Precompute image embeddings for CLIP model.

This script downloads images, computes their embeddings using CLIP,
and saves them to a safetensors file with image URLs as metadata.
"""

import json
from pathlib import Path

import torch
from PIL import Image
from safetensors.torch import save_file
from transformers import CLIPModel, CLIPProcessor


def main():
    print("Loading CLIP model...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    print("CLIP model loaded successfully!")

    # Load images from local directory
    data_dir = Path("asset/val2014")
    image_paths = sorted(data_dir.glob("*.jpg"))

    if not image_paths:
        print(f"Error: No images found in {data_dir}")
        return

    print(f"Found {len(image_paths)} images in {data_dir}")
    print(f"Processing {len(image_paths)} images...")
    images = []
    image_urls = []  # Store file paths instead of URLs
    for i, image_path in enumerate(image_paths, 1):
        print(f"  [{i}/{len(image_paths)}] Loading {image_path.name}")
        try:
            image = Image.open(image_path).convert("RGB")
            images.append(image)
            image_urls.append(str(image_path))
        except Exception as e:
            print(f"    Warning: Failed to load {image_path.name}: {e}")
            continue

    if not images:
        print("Error: No valid images loaded")
        return

    print("Computing image embeddings...")
    inputs = processor(images=images, return_tensors="pt")
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # Normalize embeddings
    image_embeddings = image_features / image_features.norm(dim=-1, keepdim=True)

    print(f"Image embeddings shape: {image_embeddings.shape}")

    # Prepare data and metadata
    save_data = {
        "embeddings": image_embeddings,
    }

    metadata = {
        "image_urls": json.dumps(image_urls),
        "model": "openai/clip-vit-base-patch32",
        "num_images": str(len(image_urls)),
    }

    # Save to safetensors
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "image_embeddings.safetensors"

    print(f"Saving embeddings to {output_path}...")
    save_file(save_data, str(output_path), metadata=metadata)

    print("✓ Precomputation complete!")
    print(f"  - Embeddings saved to: {output_path}")
    print(f"  - Number of images: {len(image_urls)}")
    print(f"  - Embedding dimension: {image_embeddings.shape[1]}")


if __name__ == "__main__":
    main()
