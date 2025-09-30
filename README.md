# Reflex + FastAPI with Admin

A minimal example project that combines:
- Reflex 0.5.x (for the web UI and app orchestration)
- An embedded FastAPI application (exposed as `app.api`)
- starlette-admin (SQLAlchemy backend) mounted at `/admin`
- SQLAlchemy 2.x ORM with SQLite by default
- Configuration via pydantic-settings from a `.env` file
- Jinja2 for admin templating, bcrypt for password hashing, httpx for HTTP testing, loguru for logging

This repository demonstrates an admin-protected area with database seeding on first run and a couple of simple API endpoints.


## Table of contents
- Overview
- Requirements
- Installation
- Environment variables
- Running the app
- Scripts
- Testing
- Project structure
- Development notes
- License


## Overview
The app is built with Reflex, which initializes an `rx.App` and embeds a FastAPI app as `app.api`. The admin UI is provided by `starlette-admin` and is mounted at `/admin`. On startup, the application checks whether the configured SQLite file exists; if not, it creates the schema and seeds the database with sample data and users.

Key endpoints:
- `/` → HTML link redirecting you to the admin (`/admin/`).
- `/api/hello` → Simple JSON payload `{"message": "Hello, World!"}`.
- `/admin` → Admin UI (login required).


## Requirements
- Python 3.11
- Recommended: Poetry for dependency management

Runtime dependencies (selected):
- reflex, fastapi, starlette-admin, sqlalchemy, pydantic-settings, httpx, jinja2, loguru, bcrypt

Notes:
- A minimal `requirements.txt` exists but only pins `reflex`. Prefer Poetry or install all runtime deps if using `pip`.


## Installation
Using Poetry (recommended):
1) Install Poetry if you don’t have it: https://python-poetry.org/docs/
2) Install dependencies:
   - `poetry install`

Using pip (alternative):
- `python -m venv .venv && source .venv/bin/activate` (on Windows: `.venv\\Scripts\\activate`)
- `pip install -U reflex fastapi starlette-admin sqlalchemy itsdangerous pydantic-settings httpx jinja2 loguru bcrypt`


## Environment variables
The app requires a `.env` file in the project root with the following keys (see `Reflex_fastapi_with_admin/configs/config.py`):
- `DATABASE_FILE` → Path to the SQLite file. Used to detect the first run and trigger seeding.
- `ENGINE_URI` → SQLAlchemy URL. Example: `sqlite:///./example.db` (the engine sets `check_same_thread=False`).
- `SECRET` → Secret key for `SessionMiddleware` (admin login session).

Example `.env` (development):
```
DATABASE_FILE=./example.db
ENGINE_URI=sqlite:///./example.db
SECRET=dev-secret-change-me
```


## Running the app
Two common options:

1) Reflex dev runner (hot reload for Reflex):
- Ensure `.env` is present.
- `poetry run reflex run` (or `reflex run` if your environment is already active)

Reflex will initialize the `rx.App` from `Reflex_fastapi_with_admin/Reflex_fastapi_with_admin.py` and start the embedded FastAPI app.

2) Uvicorn (pure API server; skips the Reflex dev UI):
- Ensure `.env` is present.
- `poetry run uvicorn Reflex_fastapi_with_admin.Reflex_fastapi_with_admin:app.api --reload`

Then open:
- API: `http://127.0.0.1:8000/api/hello`
- Admin: `http://127.0.0.1:8000/admin`

Database and seeding
- On startup, `init_database()` executes (currently wired as `on_startup=[init_database()]`). If `DATABASE_FILE` does not exist, the app creates tables and seeds sample data (articles and users: `admin`, `johndoe`, `viewer` with default password `password`).
- SQLAlchemy engine is created with `echo=True` for verbose SQL logs in development.

Static files
- Served under `/static` from `assets/static/`.
- Admin login logo path: `assets/static/logo.svg`.


## Scripts
There are no Poetry scripts defined in `pyproject.toml` at this time.
Common commands:
- Lint: `poetry run ruff check .`
- Auto-fix: `poetry run ruff check --fix .`
- Run (Reflex): `poetry run reflex run`
- Run (Uvicorn): `poetry run uvicorn Reflex_fastapi_with_admin.Reflex_fastapi_with_admin:app.api --reload`


## Testing
Lightweight approach (no server required, avoids importing `starlette-admin` if not installed):
Create a file `tests_smoke.py` in the repo root:

```
import asyncio
from fastapi.responses import HTMLResponse
from Reflex_fastapi_with_admin.api.api import hello, get_admin

def main() -> int:
    data = asyncio.run(hello())
    assert data == {"message": "Hello, World!"}
    resp = asyncio.run(get_admin())
    assert isinstance(resp, HTMLResponse)
    assert "/admin/" in resp.body.decode()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Run:
- `poetry run python tests_smoke.py`

Full-stack TestClient (requires all runtime deps, including `starlette-admin`):
```
from fastapi.testclient import TestClient
from Reflex_fastapi_with_admin.Reflex_fastapi_with_admin import app

def test_hello():
    client = TestClient(app.api)
    r = client.get("/api/hello")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, World!"}
```

Tips:
- For idempotent tests and predictable seeding, point `ENGINE_URI`/`DATABASE_FILE` to a temporary SQLite path.
- In thin CI environments, prefer the lightweight approach importing only from `Reflex_fastapi_with_admin/api/api.py`.


## Project structure
Key files and directories:
- `Reflex_fastapi_with_admin/Reflex_fastapi_with_admin.py` → Reflex entrypoint; defines `rx.App`, mounts admin and static files, wires routes.
- `Reflex_fastapi_with_admin/api/api.py` → Simple API handlers (`hello`, `get_admin`).
- `Reflex_fastapi_with_admin/configs/config.py` → `.env` settings via pydantic-settings.
- `Reflex_fastapi_with_admin/databases/database.py` → SQLAlchemy engine and Base.
- `Reflex_fastapi_with_admin/databases/seed.py` → Database seeding logic.
- `Reflex_fastapi_with_admin/models/*` → SQLAlchemy models (Article, User).
- `Reflex_fastapi_with_admin/DBViews/*` → starlette-admin views for Article and User.
- `Reflex_fastapi_with_admin/utils/*` → Auth provider for admin, logger, helpers.
- `assets/static/` → Static assets served at `/static`.
- `rxconfig.py` → Reflex config (app name, etc.).
- `pyproject.toml` → Poetry project config and dependencies.


## Development notes
- The current startup wiring uses `on_startup=[init_database()]`, which invokes the function at import time. If you need lazy execution (e.g., for some tests), consider changing it to `on_startup=[init_database]`. This README documents the current behavior without altering code.
- The SQLAlchemy engine is created with `echo=True` (see `databases/database.py`). Consider adjusting for production.


## License
TODO: Add a license file (e.g., MIT, Apache-2.0) and update this section accordingly.

If you are the project owner, choose a license and include it as `LICENSE` in the repository root, then update `pyproject.toml` with the `license` field if desired.