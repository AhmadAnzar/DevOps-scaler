# Final DevOps Project: TaskBoard

Name: Anzar
Enrollment Number: 24BCS10289

TaskBoard is a small project management app: a React frontend, a FastAPI
backend and a PostgreSQL database. The project comes from the Session 21
class repo. I ran it two ways on my Windows machine: first each part by
hand, then the whole stack with Docker Compose.

```text
Browser
   │
   ▼
Frontend (React)  ── /api ──>  Backend (FastAPI)  ──>  PostgreSQL
                               /health  /ready  /metrics  /docs
```

## Project structure

```text
Session-21/
├── backend/            FastAPI app, SQLAlchemy models, Alembic migrations, tests
├── frontend/           React + Vite app, nginx config for the container
├── docker-compose.yml  postgres + backend + frontend
├── helm/               Helm chart for Kubernetes
├── terraform/          AWS VPC + EKS
├── k8s/, monitoring/, troubleshooting/, scripts/
└── images/             my screenshots
```

## Changes I made to get it running

| Problem | Why | What I changed |
|---|---|---|
| Frontend couldn't reach the API when run manually | the Vite proxy pointed to port 8080, but the backend runs on 8000 | `frontend/vite.config.js`: proxy `/api` to `http://localhost:8000` |
| `docker compose up` failed on the database port | PostgreSQL is already installed on my Windows machine and uses 5432 | `docker-compose.yml`: publish postgres on `5433:5432` |
| Backend container exited right after starting | `depends_on` only waits for the postgres container to start, not for the database to be ready, so `alembic upgrade head` failed | added a `pg_isready` healthcheck to postgres and `condition: service_healthy` to the backend |
| Python cache files showing up in git | `.gitignore` didn't cover them | added `__pycache__/`, `.venv/` and `*.db` |

I also changed the name on the dashboard (sidebar profile, greeting and
default assignee) to mine in `frontend/src/main.jsx`.

---

## Part 1: Running it manually

### 1. Database

PostgreSQL on my machine needs its admin password to create a new user, so
I ran a separate Postgres in Docker on port 5433 with the same user,
password and database name the project expects.

```powershell
docker run -d --name taskboard-db -e POSTGRES_DB=taskboard -e POSTGRES_USER=taskboard -e POSTGRES_PASSWORD=taskboard -p 5433:5432 postgres:16-alpine
docker ps --filter name=taskboard-db
```

![postgres](images/manual-1-postgres.png)

### 2. Backend setup and migration

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg://taskboard:taskboard@localhost:5433/taskboard"
alembic upgrade head
```

Alembic ran migration `0001_create_tasks`, which creates the `tasks` table.

![backend setup](images/manual-2-backend-setup.png)

### 3. Start the backend

```powershell
uvicorn app.main:app --reload --port 8000
```

![uvicorn](images/manual-3-backend-uvicorn.png)

### 4. Start the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite serves the app on `http://localhost:5173` and forwards `/api` calls to
the backend.

![vite](images/manual-4-frontend-vite.png)

### 5. The app

I created a task from the "New task" form. It went through the backend and
got saved in PostgreSQL.

![app on 5173](images/manual-ui.png)

### 6. API docs, health and metrics

FastAPI generates Swagger docs at `/docs` with every endpoint:
`GET/POST /api/tasks`, `GET/PUT/DELETE /api/tasks/{id}`, `/api/tasks/stats`,
`/health`, `/ready` and `/metrics`.

![swagger](images/manual-docs.png)

```powershell
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/ready
curl.exe -s http://localhost:8000/metrics | Select-Object -First 25
```

- `/health` only checks that the app process is up (used for liveness).
- `/ready` also runs a query against the database, so it only says READY
  when the app can actually serve requests (used for readiness).
- `/metrics` is in Prometheus format: request counts, durations and so on.

(In PowerShell `curl` is an alias for `Invoke-WebRequest`, so I used
`curl.exe`.)

![health and metrics](images/manual-health-metrics.png)

---

## Part 2: Running it with Docker Compose

Compose starts all three services together. I stopped the manual backend,
the manual Vite server and the `taskboard-db` container first, because they
were using the same ports.

```powershell
docker stop taskboard-db
docker compose up -d --build
docker compose ps
```

### Build

The backend image installs the Python packages and runs as a non-root user
(uid 10001). The frontend uses a **multi-stage build**: the first stage uses
Node to run `npm install` and `vite build`, and the second stage only copies
the built `dist/` folder into an nginx image. Node isn't in the final image
at all.

![build 1](images/docker-compose-up1.png)

![build 2](images/docker-compose-up2.png)

![build 3](images/docker-compose-up3.png)

### All three containers running

![compose up and ps](images/docker-compose-up.png)

| Container | Port on my machine |
|---|---|
| postgres | 5433 (healthy) |
| backend | 8000 |
| frontend (nginx) | 3000 |

### The app on port 3000

Same app as before, but now nginx serves the production build from a
container, and forwards `/api` to the backend container.

![app on 3000](images/docker-ui.png)

### Stopping it

```powershell
docker compose down      # keeps the database volume
docker compose down -v   # also deletes the data
```

---

## Problems I ran into with Compose

It took a few tries to get all three containers up:

1. The backend kept exiting with
   `psycopg.OperationalError: Name or service not known`. It couldn't find
   the `postgres` host.
2. Running `docker compose up` again failed with
   `Bind for 0.0.0.0:5433 failed: port is already allocated`. My manual
   `taskboard-db` container from Part 1 was still running on 5433.
3. After stopping it, `docker compose ps` showed only 2 containers. The
   postgres container had been created during the failed attempt, so it was
   "Up" but not attached to the Compose network, which is why the backend
   couldn't resolve its name.

![only two containers](images/docker-compose-up6.png)

`docker compose down` followed by `docker compose up -d --build` recreated
the network and all three containers, and everything came up properly.

There were also some `no such host` errors pulling images from Docker Hub.
That was my internet provider's DNS. Switching Windows DNS to
`8.8.8.8` / `1.1.1.1` made it much more reliable.

## What I learned

- `depends_on` alone doesn't mean "wait until ready". It only waits for the
  container to start. A healthcheck is what actually makes the backend wait
  for the database.
- Port clashes with things already running on my laptop came up again and
  again (local PostgreSQL, old containers from class). `docker ps` and
  `netstat -ano` were the quickest way to find out what was holding a port.
- Running it by hand first made the Compose file much easier to
  understand, because I'd already done each of its steps myself.
