# NewsLens

NewsLens is an AI news intelligence platform built as a modular monolith with FastAPI, SQLAlchemy, PostgreSQL, Qdrant, and Groq.

## Architecture

The backend is organized as:

- API routes in `app/api`
- application services in `app/services`
- repositories in `app/repositories`
- infrastructure in `app/core` and `app/db`
- background jobs in `app/workers`

The full architecture guide lives in [ARCHITECTURE.md](ARCHITECTURE.md).

## Local Development

1. Configure the environment variables expected by `app/core/config.py`.
2. Run migrations with Alembic.
3. Start the FastAPI app with Uvicorn.

## Docker

Use `docker compose up --build` to start the app, PostgreSQL, Redis, and Qdrant.