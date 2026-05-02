# Contributing to EvoBrain Zero

Grazie per voler contribuire.

## Prerequisiti
- Python 3.11+
- Git

## Setup locale
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -U pip
pip install -e .[dev]
```

## Avvio applicazione
```bash
uvicorn app.main:app --reload
```

## Test
```bash
pytest
```

## Regole base
- Mantieni modifiche piccole e focalizzate.
- Aggiorna documentazione quando cambi API/comportamenti.
- Evita hardcoded di segreti o percorsi locali.
- Aggiungi test per bugfix e nuove feature.

## Workflow suggerito
1. Crea branch feature (`feat/...`) o fix (`fix/...`).
2. Esegui test locali.
3. Apri PR con descrizione chiara e impatto.
4. Collega issue correlate.
