Project-specific development guidelines

This document captures details that will speed up development and debugging for this repository. It assumes you’re an experienced Python/ASGI/Reflex/FastAPI developer and focuses only on project-specific aspects.

1) Build and configuration

Runtime stack
- App framework: Reflex 0.5.x creating rx.App with an embedded FastAPI app at app.api.
- Admin: starlette-admin (SQLAlchemy backend) mounted at /admin with a custom AuthProvider.
- ORM: SQLAlchemy 2.x; SQLite by default (thread check disabled).
- Settings: pydantic-settings reading from .env.
- Templating: Jinja2 (admin), HTTP client/testing: httpx. Logging: loguru.

Required environment (.env)
The application won’t boot correctly without these keys (see Reflex_fastapi_with_admin/configs/config.py):
- DATABASE_FILE: path to the SQLite file (used to detect “first run” and trigger seeding).
- ENGINE_URI: SQLAlchemy URL, e.g. sqlite:///./example.db (check_same_thread is set to False by the app).
- SECRET: secret key for SessionMiddleware (starlette-admin login session).

Example .env (development)
DATABASE_FILE=./example.db
ENGINE_URI=sqlite:///./example.db
SECRET=dev-secret-change-me

Install dependencies
Prefer Poetry (pyproject.toml is authoritative). The requirements.txt only pins reflex and is not sufficient to run the app.
- With Poetry:
  - Install: poetry install
  - Run commands: poetry run <command>
- With pip (if you must):
  - pip install -U reflex fastapi starlette-admin sqlalchemy itsdangerous pydantic-settings httpx jinja2 loguru bcrypt

Running the app (development)
Two convenient options:
- Reflex dev runner (hot reload for Reflex):
  - Ensure .env is present (see above).
  - reflex run
  - Reflex will initialize the rx.App (Reflex_fastapi_with_admin/Reflex_fastapi_with_admin.py) and start the embedded FastAPI app.
- Uvicorn (pure API server; skips the Reflex dev UI):
  - Ensure .env is present.
  - uvicorn Reflex_fastapi_with_admin.Reflex_fastapi_with_admin:app.api --reload

Database and seeding
- On startup, init_database() runs (wired via rx.App(on_startup=[init_database()])). It checks for DATABASE_FILE; if it does not exist, it creates all tables and calls fill_db().
- Seeding inserts:
  - Sample Article rows with random Status (see models/Article.py and databases/seed.py).
  - Users with roles and bcrypt-hashed passwords: admin, johndoe, viewer (default password: "password").
- SQL echo is enabled (engine echo=True), so expect SQL logs in dev.

Admin and authentication
- Admin is mounted under /admin and protected by MyAuthProvider (utils/provider.py).
- Login uses users stored in the database. Password verification uses bcrypt.checkpw against stored hash.
- On login, a session cookie is set; SECRET must be configured.
- Admin UI title and logo are personalized per user (see get_admin_config).

Static files
- Static assets are served under /static from assets/static/.
- Admin login_logo_url references assets/static/logo.svg (see Admin constructor).

2) Testing

Supported approaches
- Lightweight integration without spinning a server using FastAPI’s TestClient OR by directly invoking the async API callables.
- Given optional dependencies (starlette-admin) may not be installed in CI/minimal environments, tests should avoid importing the full app module unless the environment is fully provisioned.

Recommended patterns
- Direct async invocation of the API layer (preferred when admin deps aren’t available):
  Example test (standalone script):
  --- tests_smoke.py ---
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

  Run: python tests_smoke.py

- Full-stack TestClient (requires all runtime deps incl. starlette-admin):
  from fastapi.testclient import TestClient
  from Reflex_fastapi_with_admin.Reflex_fastapi_with_admin import app

  def test_hello():
      client = TestClient(app.api)
      r = client.get("/api/hello")
      assert r.status_code == 200
      assert r.json() == {"message": "Hello, World!"}

How we verified in this repo
- We executed a smoke test that directly invoked hello() and get_admin() (no server needed) to validate the API contract. This avoids importing starlette-admin in minimal environments. The test passed locally.

Adding tests
- Keep tests independent from Reflex build output. Prefer targeting pure Python callables (api/api.py) or use TestClient on app.api only when dependencies are present.
- If you need to exercise admin-protected routes, seed relies on DATABASE_FILE nonexistence. For idempotent tests, point ENGINE_URI/DATABASE_FILE to a temporary location (e.g., a tmp SQLite file) and control first-run behavior accordingly.

3) Additional development information

Project layout (key pieces)
- Reflex_fastapi_with_admin/Reflex_fastapi_with_admin.py: Reflex entrypoint defining rx.App, FastAPI integration, routes, admin mount, static files, and on_startup seeding.
- configs/config.py: .env-driven settings (DATABASE_FILE, ENGINE_URI, SECRET) via pydantic-settings.
- databases/: SQLAlchemy engine (database.py), seeding (seed.py).
- models/: SQLAlchemy models for Article and User.
- DBViews/: starlette-admin ModelView definitions for Article and User.
- utils/: LoggerSingleton (loguru formatter), provider.py (custom AuthProvider for admin).
- assets/: static files and icons.
- rxconfig.py: Reflex config (app_name).

Coding style and tooling
- Ruff is included. Run ruff check . to lint, and ruff check --fix . to auto-fix where possible. Configure additional rules in pyproject.toml if needed.
- Target Python 3.11 (per pyproject). Avoid deprecated SQLAlchemy 1.x patterns; models and sessions should use SQLAlchemy 2.x style.

Common pitfalls and tips
- Do not import Reflex_fastapi_with_admin.Reflex_fastapi_with_admin in thin CI containers unless starlette-admin and all deps are installed; import api/api.py functions for lightweight checks instead.
- Ensure .env is present before running either reflex run or uvicorn; missing SECRET will break admin sessions and may cause runtime errors.
- The on_startup wiring currently calls init_database() immediately instead of passing the callable (on_startup=[init_database()]). If you need lazy startup execution (recommended), change to on_startup=[init_database] to avoid executing at import time in certain contexts (e.g., unit tests). This is not changed now to preserve behavior, but be aware during test design.
- bcrypt hashes are expected in the users table. When creating users programmatically, store bcrypt-hashed passwords.
- SQLAlchemy engine is created with echo=True which is noisy; consider toggling via environment in production.

Reproducing a minimal test locally (what we ran)
- Create .env as above if you plan to import the full app; not required for the lightweight API function test shown here.
- Place the tests_smoke.py snippet in the repo root and run: python tests_smoke.py
- Remove the file when finished to avoid polluting the repository; this document remains as the definitive reference.

Housekeeping
- Use poetry for consistent dependency resolution; requirements.txt is intentionally minimal and not sufficient alone.
- Keep assets/static/ in sync with admin logos/avatars referenced by provider.py and Admin(config). Replace placeholders as needed.
