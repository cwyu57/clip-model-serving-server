# === Builder Stage ===
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /workspace
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# === Runtime Stage ===
FROM python:3.13-slim-trixie AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY --from=builder /workspace/.venv/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY ./app ./app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
