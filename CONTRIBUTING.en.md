# Contributing to EvoBrain Zero

> Italian version: [CONTRIBUTING.it.md](./CONTRIBUTING.it.md)

## Prerequisites
- Python 3.11+
- Git

## Local Setup
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -U pip
pip install -e .[dev]
```

## Run
```bash
uvicorn app.main:app --reload
```

## Test
```bash
pytest
```

## Ground Rules
- Keep changes focused and small.
- Update docs when behavior/API changes.
- Avoid hardcoded secrets and local-only paths.
- Add tests for bug fixes and new features.

## Suggested Workflow
1. Create feature (`feat/...`) or fix (`fix/...`) branch.
2. Run local tests.
3. Open PR with clear impact description.
4. Link related issues.
