set dotenv-load

pg-up:
    docker compose up -d postgres

pg-down:
    docker compose down postgres

pg-logs:
    docker compose logs -f postgres

local:
    just pg-up
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev:
    docker compose up app --build

migrate-create:
    #!/usr/bin/env bash
    REVISION=$(uv run python -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:-3])")
    MIGRATION_NAME=$(gum input --placeholder "Enter migration name")
    uv run alembic revision --rev-id "${REVISION}" -m "${MIGRATION_NAME}"

migrate:
    uv run alembic upgrade head

migrate-alembic-current:
    uv run alembic current

migrate-alembic-upgrade-by-one:
    uv run alembic upgrade +1

migrate-alembic-downgrade-by-one:
    uv run alembic downgrade -1

sqlacodegen-models:
    #!/usr/bin/env bash
    OUTPUT_FILE="${1:-app/entity/model/generated.py}"
    : "${POSTGRES_USER:?POSTGRES_USER is not set}"
    : "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is not set}"
    : "${POSTGRES_DB:?POSTGRES_DB is not set}"
    : "${POSTGRES_HOST:?POSTGRES_HOST is not set}"
    : "${POSTGRES_PORT:?POSTGRES_PORT is not set}"
    DATABASE_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    echo "Generating models from database: ${DATABASE_URL}"
    uv run sqlacodegen "${DATABASE_URL}" --outfile "${OUTPUT_FILE}"
    echo "Models generated to: ${OUTPUT_FILE}"
