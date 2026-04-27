# EduLingo AI

AI-powered language learning platform with real-time speech coaching, spaced-repetition flashcards, and adaptive lesson generation.

## Tech stack

- **Frontend** — Next.js 16 (App Router), TypeScript, Tailwind v4, React Query, Zustand
- **Backend** — FastAPI, SQLAlchemy 2 (async), PostgreSQL 16, Redis 7; hexagonal / clean architecture
- **AI** — Google Gemini (tutor, writing rubric), Whisper + wav2vec2 (ASR + phoneme alignment), librosa (pitch)
- **Storage** — MinIO (S3-compatible audio storage)
- **Infra** — Docker Compose

---

## Quick start (Docker, one command)

```bash
./scripts/docker-stack.sh up
```

The script copies `.env.example` → `.env` on first run, builds all images, starts the stack detached, waits for every service to become healthy, and finally runs smoke tests against each exposed port. Expect 3–8 min on the first build, < 30 s on subsequent runs.

Sub-commands:

| Command | What it does |
|---|---|
| `./scripts/docker-stack.sh up`    | build, start, wait healthy, smoke-test |
| `./scripts/docker-stack.sh test`  | run smoke tests against a running stack |
| `./scripts/docker-stack.sh logs`  | `docker compose logs -f` (append service name to filter) |
| `./scripts/docker-stack.sh down`  | stop containers (volumes kept) |
| `./scripts/docker-stack.sh clean` | stop + remove named volumes (nuke DB + MinIO data) |

Service URLs once up:

| Service | URL | Notes |
|---|---|---|
| Frontend (Next.js) | http://localhost:3000 | public UI |
| Backend (FastAPI)  | http://localhost:8000 | REST API |
| Swagger UI         | http://localhost:8000/docs | interactive API explorer |
| OpenAPI JSON       | http://localhost:8000/api/openapi.json | |
| MinIO console      | http://localhost:9001 | login with `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` from `.env` |
| MinIO S3 API       | http://localhost:9000 | |

Set `GEMINI_API_KEY` in `.env` before exercising the Gemini-backed features (lesson generation, writing rubric).

---

## Run locally (native, no Docker)

Useful for fast iteration with hot reload. You still need Postgres, Redis, and MinIO running — easiest is to start just those via Compose:

```bash
docker compose up -d postgres redis minio minio-bootstrap
```

Then run backend and frontend natively in two shells:

```bash
# shell 1 — backend
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

```bash
# shell 2 — frontend
cd frontend
pnpm install
pnpm dev
```

When running natively, point the backend at the local services by overriding URLs in `.env`:

```
DATABASE_URL=postgresql+asyncpg://edulingo:edulingo@localhost:5432/edulingo
REDIS_URL=redis://localhost:6379/0
MINIO_ENDPOINT_URL=http://localhost:9000
```

---

## Running the tests

```bash
# backend: ruff + mypy + pytest (unit + integration + e2e)
cd backend
uv run ruff check .
uv run mypy app
uv run pytest -m "unit or integration or e2e"

# frontend: types + lint + vitest
cd ../frontend
pnpm tsc --noEmit
pnpm lint
pnpm vitest run
```

The Docker smoke tests (`./scripts/docker-stack.sh test`) are a stricter subset: they verify every exposed port is actually serving traffic end-to-end.

---

## Demo walkthrough

A 3-minute tour that exercises the full stack (frontend → backend → Postgres → MinIO → Gemini).

### 1. Bring the stack up

```bash
./scripts/docker-stack.sh up
```

Wait for the `all smoke tests passed` line.

### 2. Seed demo accounts

There are no accounts out of the box. Run:

```bash
./scripts/docker-stack.sh seed
```

| Email | Password | Role | Use for |
|---|---|---|---|
| `demo@edulingo.ai` | `password123` | learner | `/library`, `/today`, onboarding |
| `admin@edulingo.ai` | `admin12345` | admin | `/admin`, content generation |

The `seed` subcommand is idempotent — running it twice is safe; existing users are left untouched. Accounts live in the Postgres volume, so `./scripts/docker-stack.sh clean` wipes them and you'll need to re-seed. Passwords above are dev-only; change them before exposing anything.

Log in at http://localhost:3000/login.

### 3. Generate content with Gemini

1. Make sure `GEMINI_API_KEY=...` is set in `.env` and restart backend: `docker compose restart backend`.
2. Open http://localhost:3000/admin/content/generate
3. Fill in target CEFR, topic, length → **Generate**. The backend calls Gemini, stores the piece draft in Postgres, and (if generated) writes audio to MinIO at `edulingo-audio/pieces/<piece_id>/audio-<uuid>.mp3`. Check it in the MinIO console at http://localhost:9001.
4. Review the draft, click **Publish**.

### 4. Read it as a learner

Log out, log in as `demo@edulingo.ai` / `password123`, go to http://localhost:3000/library, and open the published piece. Audio is served via time-limited MinIO presigned URLs.

### 5. Explore the API directly

Swagger UI (http://localhost:8000/docs) lists every route, grouped by tag:

| Tag | Prefix | Highlights |
|---|---|---|
| `auth` | `/api/auth` | `register`, `login`, `logout`, `me` (GET/PATCH) |
| `library` | `/api/library` | list + read published pieces (learner side) |
| `admin-content` | `/api/admin/content` | CRUD, `publish`, `archive`, `media` upload, generation |

### 6. Tear down

```bash
./scripts/docker-stack.sh down      # keep data for tomorrow
./scripts/docker-stack.sh clean     # nuke volumes (fresh DB + MinIO)
```

---

## Troubleshooting

- **Port already in use** — something else is on 3000/8000/9000/9001/5432/6379. `lsof -i :8000` to find it, or override the `ports:` mapping in `docker-compose.yml`.
- **Backend unhealthy during `up`** — run `./scripts/docker-stack.sh logs backend`. Most often: bad `DATABASE_URL`, or Alembic migration failure.
- **MinIO bucket missing in smoke test** — the `minio-bootstrap` service creates it on first boot; re-run `docker compose up -d minio-bootstrap`.
- **Gemini errors** — `GEMINI_API_KEY` unset or rate-limited. Non-AI flows work without it.
