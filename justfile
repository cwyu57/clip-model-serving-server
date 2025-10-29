set dotenv-load


pg-up:
    docker compose up -d postgres

pg-down:
    docker compose down postgres

pg-logs:
    docker compose logs -f postgres
