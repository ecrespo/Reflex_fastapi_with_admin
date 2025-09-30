# Dependency Audit — 2025-09-30

This report inventories dependencies for all package managers in this repository, summarizes known vulnerabilities (if any), and highlights available updates grouped by impact. Where automated scanners were unavailable in the current environment, we provide clear commands to reproduce the audit locally.

Repository: Reflex_fastapi_with_admin
Generated: 2025-09-30 19:25 local time

---

## Package managers detected

- Poetry (pyproject.toml + poetry.lock) — primary dependency manager
- pip requirements (requirements.txt) — minimal, overrides/pins only

---

## Inventory

### Direct dependencies (pyproject.toml)
The following are declared direct runtime dependencies and their specified version constraints:

- python = ^3.11
- ruff = ^0.4.10
- mongoengine = ^0.28.2
- starlette-admin = ^0.14.0
- fastapi = ^0.111.0
- reflex = ^0.5.4
- sqlalchemy = ^2.0.31
- itsdangerous = ^2.2.0
- pydantic-settings = ^2.3.3
- httpx = ^0.27.0
- jinja2 = ^3.1.4
- loguru = ^0.7.2
- bcrypt = ^4.1.3

### Resolved dependency set (from poetry.lock)
- Total resolved packages: 103
- Lockfile tool: Poetry 1.8.2

Note: The full transitive list is available in poetry.lock. For brevity, only direct dependencies are expanded in this report.

### requirements.txt
- reflex==0.5.4

---

## Vulnerability audit

Automated CVE scanning tools (pip-audit/safety) were not available in the current execution environment, so no live lookup against vulnerability databases was performed here. To reproduce a full audit locally and include CVE IDs, severity, and fixed versions, run one of the following:

Using pip-audit (recommended):
- pip install pip-audit
- pip-audit -r requirements.txt
- pip-audit -P  # scan the active environment (after `poetry install`)
- pip-audit -f json > pip-audit-report.json  # machine-readable output

Using Safety:
- pip install safety
- safety check --full-report
- safety check -r requirements.txt --json > safety-report.json

If you run these and share the JSON, we can enrich this report with explicit vulnerability entries (ID, severity, fixed versions) and targeted remediation guidance.

Known security-sensitive packages in this stack and typical watchpoints:
- fastapi/starlette: occasional request validation or header parsing CVEs; ensure Starlette and Pydantic are in compatible, patched versions.
- httpx/anyio: TLS and redirect handling CVEs may arise; keep patch-level current.
- Jinja2: template sandbox escapes; keep at latest 3.1.x.
- SQLAlchemy: ORM/type CVEs; stay on latest 2.0.x.
- bcrypt: keep to the latest 4.1.x+

---

## Update availability and impact

Live “outdated” checks were not available in the current environment. Below are recommended commands and a best‑effort qualitative assessment. We can run these locally if you prefer, or you can run and paste the output for us to incorporate.

Check with Poetry:
- poetry install
- poetry show --outdated  # concise
- poetry show --tree      # see transitive graph

Check with pip (if using requirements):
- python -m pip list --outdated

Best‑effort expectations (may not reflect the very latest without live queries):
- fastapi ^0.111.x: Minor/patch updates likely available. Minor bumps in FastAPI are typically backward compatible but can deprecate behaviors (watch Starlette compatibility).
- starlette-admin ^0.14.x: Minor/patch updates may be available. Admin UIs occasionally introduce breaking changes on majors; we’d batch any major separately.
- sqlalchemy ^2.0.31: Patch updates within 2.0.x expected; these are safe to apply.
- httpx ^0.27.x: Patch/minor updates likely; usually safe but check timeout and redirect behaviors.
- reflex ^0.5.4: Patch/minor updates may include build/runtime changes for the dev server; review changelog before minor bumps.
- ruff ^0.4.10: Rapid release cadence; patch/minors available. Lint rules can tighten; may affect CI formatting/lint checks.
- jinja2 ^3.1.4, itsdangerous ^2.2.0, loguru ^0.7.2, bcrypt ^4.1.3, pydantic-settings ^2.3.3: Patch/minor updates likely available; generally safe.

Major version changes (to be skipped/batched):
- Any move to FastAPI 1.x (if/when published) or Starlette-admin 1.x would be considered breaking until validated.
- SQLAlchemy 3.x (future) would be a breaking change; stick to 2.0.x for now.
- Pydantic 3.x (future) would be breaking; pydantic-settings tracks Pydantic major versions.

---

## Recommended next actions

1) Approve running automated scanners and update checks so we can enrich this report with concrete CVE IDs and fixed versions:
- pip-audit -P and/or safety check
- poetry show --outdated

2) With your approval, we will prepare a patch/minor update PR that:
- Bumps patch/minor versions only within the current major for all direct deps listed above.
- Regenerates poetry.lock via `poetry update` (scoped to safe ranges) and ensures requirements.txt remains consistent (reflex pin).
- Runs smoke tests (per README guidelines) to ensure app still boots; we’ll avoid importing full app if admin deps are missing.

3) Major updates will be proposed separately with notes on breaking changes and a migration plan.

---

## Appendix — How to keep this report fresh

- Re-run this report after dependency changes using:
  - pip-audit -f json > pip-audit-report.json
  - poetry show --outdated > poetry-outdated.txt
  - Then share the outputs; we’ll update this Markdown with concrete vulnerability details and upgrade actions.

