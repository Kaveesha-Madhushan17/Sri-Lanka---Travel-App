# Tour Sri — Sri Lanka Travel Web App

Everything a traveller needs for Sri Lanka, in one place. See [PLAN.md](PLAN.md) for the full plan.

**Stack:** Next.js 15 (frontend) · FastAPI / Python 3.12 (backend) · PostgreSQL 16 + pgvector · Docker Compose

## Requirements
- Docker and Docker Compose v2

## Run (development)
```bash
cp .env.example .env                             # first time only
docker compose up --build -d                     # builds images and starts db, backend, frontend
docker compose exec backend alembic upgrade head # run database migrations
docker compose exec backend python scripts/seed.py # seed 6 regions, 6 categories, 25 places
```

| Service  | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Destinations list | http://localhost:3000/destinations |
| Sigiriya detail page | http://localhost:3000/destinations/sigiriya |
| API docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/v1/health |

Code changes reload automatically (source folders are mounted into the containers).

## Useful commands
```bash
docker compose logs -f backend               # follow backend logs
docker compose exec backend pytest           # run backend tests
docker compose exec frontend npm run generate:types # regenerate TypeScript types from OpenAPI
docker compose down                          # stop containers
docker compose down -v                       # stop AND delete the database volume
docker compose build frontend                # rebuild after adding npm packages
```

## Structure
```
frontend/   Next.js app (UI only, calls the API)
backend/    FastAPI app (business logic, database, AI)
```

