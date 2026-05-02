# EvoBrain Zero

EvoBrain Zero is a local cognitive platform (FastAPI + SQLAlchemy) designed as a traceable, controllable "second brain" foundation.

> Italian version: [README.it.md](./README.it.md)

## Project Status
Active prototype with modular APIs, local SQLite persistence, operational UI, audit support, and test suite.

## Stack
- Python 3.11+
- FastAPI
- SQLAlchemy 2
- Alembic
- Pydantic 2
- Pytest

## Quickstart
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -U pip
pip install -e .[dev]
uvicorn app.main:app --reload
```

Main UI endpoints:
- `http://127.0.0.1:8000/api/v1/ui/dashboard`
- `http://127.0.0.1:8000/api/v1/ui/graph`
- `http://127.0.0.1:8000/api/v1/ui/chat`
- `http://127.0.0.1:8000/api/v1/ui/audit`

## Recommended Usage
Preferred channel for deep LLM iteration: **agentic IDE workflow** (code + terminal + tests).

Chat UI is suitable for quick interactions and operational commands, but has natural limits for deep multi-file development loops.

## Ebby Mode
For Ebby activation/baptism flow and internal help:
- [docs/EBBY_MODE.en.md](./docs/EBBY_MODE.en.md)
- [docs/EBBY_INTERNAL_HELP.en.md](./docs/EBBY_INTERNAL_HELP.en.md)

## Tests
```bash
pytest
```

## Repository Structure
```text
app/                # API, services, models, orchestration
alembic/            # DB migrations
directive/          # governance and architecture directives (authoritative in Italian)
tests/              # test suite
.github/            # CI and templates
```

## Configuration
- Copy `.env.example` to `.env` if needed.
- Local DB is under `data/db/` (excluded from versioning).

## GitHub Publishing Checklist
1. Create remote repository.
2. Set default branch (`main`).
3. Enable GitHub Actions.
4. Enable secret scanning and Dependabot (recommended).
5. Initial push:
   ```bash
   git init
   git add .
   git commit -m "chore: bootstrap repository for github"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

## Governance and Docs
- [CONTRIBUTING.it.md](./CONTRIBUTING.it.md)
- [CONTRIBUTING.en.md](./CONTRIBUTING.en.md)
- [SECURITY.it.md](./SECURITY.it.md)
- [SECURITY.en.md](./SECURITY.en.md)
- [CHANGELOG.it.md](./CHANGELOG.it.md)

## License
[MIT](./LICENSE)

