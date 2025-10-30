set dotenv-load


pg-up:
    docker compose up -d postgres

pg-down:
    docker compose down postgres

pg-logs:
    docker compose logs -f postgres


# Run entire app stack in Docker (app + infrastructure)
dev:
    docker compose up app --build


migrate-create:
    #!/usr/bin/env bash
    REVISION=$(uv run python -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:-3])")
    MIGRATION_NAME=$(gum input --placeholder "Enter migration name")
    uv run alembic revision --rev-id "${REVISION}" -m "${MIGRATION_NAME}"

migrate-alembic-current:
    uv run alembic current

migrate-alembic-upgrade-by-one:
    uv run alembic upgrade +1

migrate-alembic-downgrade-by-one:
    uv run alembic downgrade -1
