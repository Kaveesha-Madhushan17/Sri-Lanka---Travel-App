# Sri Lanka Travel Web App — Implementation Plan

> **Vision:** Everything a traveller needs for Sri Lanka, in one place, with minimum effort.
>
> A learn-by-doing project: build one phase at a time, understand the code, then move on.
> Web app first, mobile app (Expo) later using the same backend API.
> Everything runs in Docker so it can be hosted on any server later.

---

## 1. Goals

1. Make Sri Lanka easy to understand for a first-time visitor (regions, seasons, culture, transport).
2. Make information **easy to find**: good search, filters, map, clear pages.
3. Give **accurate, local, practical** information (fees, travel times, honest tips).
4. Add **AI agents** that use real data: a RAG Concierge chat and a Trip Planner agent with tool calling.
5. One backend API shared by the web app and the future mobile app.
6. **Host-agnostic:** no vendor lock-in; the whole system starts with `docker compose up`.

---

## 2. Features

### A. Core features
| Feature | Description |
|---|---|
| Destinations explorer | Pages for each place: photos, description, entry fees (foreign/local), best time, recommended duration, tips |
| Interactive map | All places on a map, filter by category |
| Search & filters | Search by name/tags; filter by category, region, month |
| Season guide | Select a month → shows best coast/regions (SW monsoon May–Sep, NE monsoon Oct–Jan) |
| Getting around | Main train routes (Colombo–Kandy, Kandy–Ella, Colombo–Galle), buses, tuk-tuk fare guide, PickMe/Uber, driver hire |
| Culture & etiquette | Temple dress code, Buddha image rules, Poya days (no alcohol sales), shoes off, greetings |
| Essentials | ETA visa, money/ATMs, SIM cards, emergency numbers, safety |
| Food guide | Rice & curry, kottu, hoppers, string hoppers, spice level, where to try |
| Favourites & My Trips | Logged-in users save places and itineraries |
| Live weather | Current weather by region on destination pages |
| Admin panel | Admin users add/edit places, articles, foods and upload images (Cloudinary) |

### B. AI features
| Feature | Description |
|---|---|
| AI Concierge (RAG) | Chat that answers only from the app's own verified data, shows source links, says when it doesn't know |
| Trip Planner Agent | Input: days, interests, budget, start city, month → agent calls tools and returns a structured day-by-day itinerary with a map |
| Budget Agent | Estimates total trip cost (transport, entry fees, accommodation range) |
| Re-planner | Suggests alternatives when weather is bad |
| Photo Lens | Upload a photo of food/place → explains what it is |
| Phrase helper | Useful Sinhala & Tamil phrases with pronunciation |

### C. Later / extras
- Festival & Poya calendar (Esala Perahera, Vesak, etc.)
- Trip sharing via link
- PWA offline mode
- Multi-language (English, German, French, Chinese, Russian)
- Local business listings & traveller reviews
- Mobile app (React Native / Expo)

---

## 3. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | **Next.js 15 (App Router) + TypeScript** — frontend only | SEO matters for a tourism site; server rendering for fast pages |
| UI | Tailwind CSS + shadcn/ui | Fast, clean, consistent UI |
| Maps | react-leaflet + OpenStreetMap | Free, no billing |
| Backend | **Python 3.12 + FastAPI** | Best ecosystem for AI agents/embeddings; async; automatic OpenAPI (Swagger) docs |
| Package manager (Python) | uv | Fast, reproducible installs |
| Database | **PostgreSQL 16 + pgvector** | Relational data and vector search in one database |
| ORM & migrations | SQLAlchemy 2.0 (async) + Alembic | Industry standard |
| Validation | Pydantic v2 (backend), zod (frontend forms) | Typed, validated data on both sides |
| Auth | JWT (access + refresh tokens in httpOnly cookies), password hashing with Argon2, Google OAuth | Learn how auth really works; no vendor dependency |
| Image storage | **Cloudinary** (free tier) | Image hosting, resizing and CDN; accessed through an image-service module so it can be swapped later (e.g. S3) |
| AI | LLM provider wrapper in the backend (start with Gemini API free tier; swappable via env vars) | Avoid lock-in to one AI provider |
| Weather | Open-Meteo (free, no API key), proxied and cached by the backend | |
| API types | openapi-typescript (generate frontend types from FastAPI's OpenAPI schema) | Frontend and backend stay in sync |
| Testing | pytest + httpx (backend), Playwright later (frontend) | |
| Containers | **Docker + Docker Compose** | Same setup on laptop and any server |
| Reverse proxy (production) | Caddy | Automatic HTTPS, one domain for frontend + API |
| Mobile (later) | React Native (Expo) | Calls the same FastAPI backend |

---

## 4. Architecture

```
                ┌──────────────────── Docker Compose ─────────────────────┐
User ──► Caddy (prod only, HTTPS)                                          │
            │                                                              │
            ├──► frontend  (Next.js)  ──── calls ───┐                      │
            │                                       ▼                      │
            └──► /api ──────────────────────► backend (FastAPI)            │
                                                 │      │                  │
                                                 │      └──► db (PostgreSQL + pgvector)
                └────────────────────────────────┼─────────────────────────┘
                                                 ├──► Cloudinary (images)
                                                 ├──► LLM API (Gemini, swappable)
                                                 └──► Open-Meteo (weather)

Mobile app (later) ─────────────────────────────► backend (same API)
```

**Principles**
- The **backend owns all business logic, data access, auth and AI**. The frontend only displays data and calls the API.
- The frontend never talks to the database, Cloudinary secrets or the LLM directly.
- API versioned under `/api/v1`.

---

## 5. Project Structure (monorepo)

```
sri-lanka-travel/
├── frontend/                       # Next.js app
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx            # Home
│   │   │   ├── destinations/       # list + [slug] detail
│   │   │   ├── map/
│   │   │   ├── getting-around/
│   │   │   ├── culture/
│   │   │   ├── essentials/
│   │   │   ├── food/
│   │   │   ├── plan/               # AI Trip Planner
│   │   │   ├── chat/               # AI Concierge
│   │   │   ├── my-trips/
│   │   │   ├── login/ register/
│   │   │   └── admin/              # Admin panel
│   │   ├── components/
│   │   ├── lib/api/                # Typed API client
│   │   └── types/                  # Generated from OpenAPI
│   ├── Dockerfile
│   └── package.json
│
├── backend/                        # FastAPI app
│   ├── app/
│   │   ├── main.py
│   │   ├── core/                   # config (pydantic-settings), security, logging
│   │   ├── db/                     # engine, session, base
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── api/v1/routers/         # places, regions, categories, articles, foods,
│   │   │                           # routes, weather, auth, users, favourites,
│   │   │                           # itineraries, admin, chat, plan
│   │   ├── services/               # business logic, image_service (Cloudinary), weather_service
│   │   └── ai/
│   │       ├── llm.py              # provider wrapper
│   │       ├── embeddings.py
│   │       ├── rag.py
│   │       ├── tools/              # search_places, get_weather, get_travel_time, get_place_details
│   │       └── agents/             # trip_planner
│   ├── alembic/                    # migrations
│   ├── scripts/
│   │   ├── seed.py                 # seed data
│   │   └── embed.py                # build embeddings
│   ├── seed_data/                  # JSON files with places, foods, articles, routes
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
│
├── caddy/Caddyfile                 # production reverse proxy
├── docker-compose.yml              # development
├── docker-compose.prod.yml         # production overrides
├── .env.example
├── .gitignore
├── README.md
└── PLAN.md
```

---

## 6. Docker Setup

**Development (`docker-compose.yml`)**
| Service | Image / build | Notes |
|---|---|---|
| `db` | `pgvector/pgvector:pg16` | Named volume for data, healthcheck |
| `backend` | `./backend` | Hot reload (`uvicorn --reload`), source mounted, depends on `db` healthy, port 8000 |
| `frontend` | `./frontend` | Hot reload (`next dev`), source mounted, port 3000 |

**Production (`docker-compose.prod.yml`)**
- Multi-stage Dockerfiles, non-root users, Next.js `output: "standalone"`
- Backend runs with multiple workers, no reload
- `caddy` service in front with automatic HTTPS
- DB not exposed to the internet; daily `pg_dump` backup
- Works on any VPS (AWS EC2/Lightsail, DigitalOcean, Hetzner, etc.) — hosting decided later

**Common commands**
```
docker compose up --build              # start everything
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed.py
docker compose logs -f backend
```

---

## 7. Database Design

| Table | Main columns |
|---|---|
| `regions` | id, name, slug, province, description, best_months (int[]), latitude, longitude |
| `categories` | id, name, slug, icon — Beach, Culture & Heritage, Wildlife, Hiking, Nature, City |
| `places` | id, name, slug, region_id, short_description, description, latitude, longitude, entry_fee_foreign_usd, entry_fee_local_lkr, best_time_to_visit, recommended_duration_hours, tips (text[]), tags (text[]), is_published, created_at, updated_at |
| `place_categories` | place_id, category_id |
| `images` | id, owner_type (place/food/article), owner_id, cloudinary_public_id, url, alt_text, sort_order |
| `foods` | id, name, slug, description, spice_level (1–5), where_to_try |
| `travel_routes` | id, from_location, to_location, mode (train/bus/tuk/car), duration_minutes, approx_cost_lkr, notes |
| `articles` | id, title, slug, section (culture / essentials / getting-around), content (markdown), updated_at |
| `users` | id, email, password_hash (nullable for Google users), display_name, country, role (user/admin), google_id, created_at |
| `refresh_tokens` | id, user_id, token_hash, expires_at, revoked |
| `favourites` | user_id, place_id, created_at |
| `itineraries` | id, user_id, title, days, preferences (jsonb), data (jsonb), share_token, created_at |
| `knowledge_chunks` | id, source_type, source_id, content, embedding (vector — dimension must match the embedding model) |

**Notes**
- Sri Lanka has no official public train API → main routes are stored manually in `travel_routes`.
- Authorization is enforced in the backend: every user-owned query filters by the current user's id; admin routes require `role = admin`.
- Seed data lives in JSON files (`backend/seed_data/`) so it is easy to read, review and correct.

---

## 8. API Overview (`/api/v1`)

| Area | Endpoints (examples) |
|---|---|
| Health | `GET /health` |
| Content | `GET /places`, `GET /places/{slug}`, `GET /regions`, `GET /categories`, `GET /foods`, `GET /articles?section=`, `GET /routes` |
| Search | `GET /places?q=&category=&region=&month=` |
| Weather | `GET /weather?lat=&lng=` (cached) |
| Auth | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/google`, `GET /auth/me` |
| User | `GET/POST/DELETE /favourites`, `GET/POST/DELETE /itineraries` |
| Admin | CRUD for places, articles, foods, routes; `POST /admin/images` (Cloudinary upload) |
| AI | `POST /chat` (streaming, SSE), `POST /plan` |

Interactive docs at `http://localhost:8000/docs`.

---

## 9. Phases

Each phase ends with something working. Commit to Git after each phase.

### Phase 0 — Setup & Docker (3–4 days)
- Monorepo with `frontend/` and `backend/`
- FastAPI app with `GET /api/v1/health`, config via pydantic-settings
- Next.js + Tailwind + shadcn/ui, layout (navbar, footer), home page "Discover Sri Lanka" that shows the backend health status
- Dev Dockerfiles + `docker-compose.yml` (db, backend, frontend) with hot reload
- `.env.example`, `.gitignore`, `README.md`
- ✅ Done when: `docker compose up` shows the home page at :3000 and Swagger at :8000/docs

### Phase 1 — Database & Destinations (1–2 weeks)
- SQLAlchemy models + Alembic migrations for content tables (enable pgvector extension)
- Seed JSON + `scripts/seed.py` with 20–30 real places across regions and categories (placeholder image URLs for now)
- Content endpoints (places, regions, categories)
- Typed API client in the frontend (types generated from OpenAPI)
- Home page (hero, categories, featured places), destinations list, destination detail page
- pytest tests for the places endpoints
- ✅ Done when: the Sigiriya page shows fees, best time, duration and tips from the API

### Phase 2 — Easy to Find (1–2 weeks)
- Search by name/tags (PostgreSQL full-text search)
- Filters: category, region, month — kept in the URL query string
- `/map` with react-leaflet, category-coloured markers
- Season guide (month → best regions)
- ✅ Done when: filtering "Beach + August" shows east coast places

### Phase 3 — Practical Information & Weather (1 week)
- Models, migrations, seed data for foods, articles, travel_routes
- `/getting-around`, `/culture`, `/essentials`, `/food` pages
- Weather service: backend calls Open-Meteo with caching; weather widget on destination pages
- ✅ Done when: a destination page shows today's weather

### Phase 4 — Users, Auth & Admin (1–2 weeks)
- Users, refresh tokens; register/login/logout/refresh with JWT in httpOnly cookies; Argon2 password hashing
- Google OAuth login
- Favourites and `/my-trips`
- Admin role + admin panel: CRUD for places/articles/foods/routes
- Cloudinary image upload through the backend `image_service`; replace placeholder images
- Rate limiting on auth endpoints
- ✅ Done when: a user logs in and saves a place; an admin uploads an image for a place

### Phase 5 — AI Concierge / RAG (2 weeks)
- LLM provider wrapper (`app/ai/llm.py`) and embeddings module
- `scripts/embed.py`: chunk places, articles, foods → embeddings → `knowledge_chunks`
- `POST /chat`: question → embed → pgvector similarity search → LLM with retrieved context → streamed answer (SSE)
- `/chat` UI with streaming messages, source links and example questions
- Answers only from retrieved data; says when it doesn't know
- ✅ Done when: "Can I visit Sigiriya with kids?" is answered from the app's data with sources

### Phase 6 — Trip Planner Agent (2–3 weeks)
- Tools: `search_places`, `get_place_details`, `get_weather`, `get_travel_time`
- Agent loop written by hand (call LLM → run requested tools → feed results back → repeat until done, with a max-step limit) so the concept is clear
- Input: days, interests, budget, starting city, travel month
- Output: Pydantic-validated JSON itinerary → day-by-day view + map in the frontend
- Logged-in users save itineraries; tool calls are logged for debugging
- ✅ Done when: "7 days, nature, medium budget, from Colombo, in March" returns a realistic plan

### Phase 7 — Production Readiness (1 week)
- Multi-stage production Dockerfiles, `docker-compose.prod.yml`, Caddy with HTTPS
- Security headers, CORS, rate limits, structured logging, error handling
- Database backup script
- GitHub Actions: run tests and build images on every push
- ✅ Done when: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up` runs the full production setup locally

### Phase 8 — Extras (ongoing)
- Budget agent, re-planner, photo lens, phrase helper
- Festival & Poya calendar
- PWA offline mode, multi-language, trip sharing

### Phase 9 — Mobile App
- Expo app using the same FastAPI backend

---

## 10. Rules for Development

1. Work on **one phase at a time**.
2. Everything runs in Docker; the README must explain how to start it.
3. Secrets only in `.env`; keep `.env.example` updated; never hardcode or commit keys.
4. Backend owns business logic, auth and AI; frontend only calls the API.
5. Mobile-first, responsive, accessible UI; clean, nature-inspired design.
6. Mark uncertain data (fees, times) with `"TODO: verify"` so it can be checked by hand.
7. Write tests for backend endpoints as features are added.
8. Commit to Git after every phase.
9. After each phase: list created files, explain how to run/test, list concepts to study.

---

## 11. Learning Outcomes per Phase

| Phase | What you learn |
|---|---|
| 0 | Monorepo structure, Docker, Docker Compose, FastAPI & Next.js basics |
| 1 | Database design, SQLAlchemy, Alembic migrations, REST API design, typed API clients |
| 2 | Full-text search, filtering, maps, UX for findability |
| 3 | Calling external APIs, caching |
| 4 | Authentication (JWT, refresh tokens, OAuth), authorization, file uploads, admin CRUD |
| 5 | Embeddings, vector search, RAG, streaming (SSE) |
| 6 | AI agents, tool calling, agent loops, structured outputs |
| 7 | Production Docker, reverse proxy, HTTPS, CI/CD, backups |
| 8–9 | PWA, i18n, React Native |
