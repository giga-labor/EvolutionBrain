# EvoBrain Zero
[![CI](https://github.com/giga-labor/EvolutionBrain/actions/workflows/ci.yml/badge.svg)](https://github.com/giga-labor/EvolutionBrain/actions/workflows/ci.yml)

EvoBrain Zero e una piattaforma cognitiva locale basata su FastAPI + SQLAlchemy, progettata come base per un "secondo cervello" esterno, tracciabile e controllabile.

> English version: [README.en.md](./README.en.md)

## Stato progetto
Implementazione in corso con API modulari, persistenza locale SQLite, UI operativa, audit e suite test.

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
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -U pip
pip install -e .[dev]
uvicorn app.main:app --reload
```

UI principali:
- `http://127.0.0.1:8000/api/v1/ui/dashboard`
- `http://127.0.0.1:8000/api/v1/ui/graph`
- `http://127.0.0.1:8000/api/v1/ui/chat`
- `http://127.0.0.1:8000/api/v1/ui/audit`

## Modalita d'uso consigliata
Per iterare rapidamente con LLM e far evolvere il sistema in modo controllato, l'uso consigliato e una **interfaccia agentica/IDE** con accesso al codice e al terminale.

Esempi tipici:
- IDE con agente (es. VS Code + estensioni agentiche)
- ambienti agentici dedicati per coding/reasoning
- terminale + assistente LLM con contesto repository

Perche e preferibile:
- accesso completo alla struttura del progetto (`app/`, `directive/`, `tests/`, `alembic/`)
- modifiche, test e debug nello stesso loop
- iterazione piu veloce su prompt, codice, verifiche e refactor
- migliore tracciabilita delle decisioni tecniche
- conoscenza concettuale indipendente dalla lingua, con resa linguistica dinamica via LLM

## Procedura di impiego iniziale (modalita Ebby)
Per avviare correttamente una nuova sessione LLM:
1. Fai leggere struttura repo + documenti `directive/`.
2. Chiedi attivazione esplicita della voce "Ebby".
3. Imposta policy operative (tracciabilita, controllo, distinzione epistemica).
4. Imposta policy DB (funzioni Python interne prima di SQL diretto).
5. Richiedi conferma breve su identita/ruolo/limiti.

Prompt rapido consigliato:
```text
Leggi il progetto EvoBrain Zero e attiva la modalita Ebby.
Nome: Ebby. Ruolo: secondo cervello operativo.
Lavora con tracciabilita, controllo umano e distinzione tra fatto/inferenza/ipotesi/scenario/azione.
Per il DB usa prima funzioni Python interne al progetto.
Conferma in 4 righe chi sei, cosa fai, limiti e canale consigliato.
```

Guida completa: [docs/EBBY_MODE.it.md](./docs/EBBY_MODE.it.md)

## Uso via Chat UI (quando usarla e limiti)
La Chat UI e utile per operazioni veloci e consultazione, ma ha limiti naturali rispetto a un flusso agentico in IDE:
- contesto tecnico piu ristretto rispetto all'intero repository
- minore controllo su refactor multi-file e verifiche profonde
- meno adatta a cicli lunghi di implementazione/test

In sintesi:
- **IDE/agentico**: canale principale per sviluppo e iterazione LLM
- **Chat UI**: canale rapido operativo, con profondita inferiore

## Vantaggio LLM su lingua e concetti
EvoBrain conserva la conoscenza come **concetti strutturati** (livello stabile), mentre l'LLM traduce/adatta la risposta nella lingua dell'utente (livello espressivo).

Effetto pratico:
- stessa base concettuale riusabile con utenti multilingua
- minore frammentazione della conoscenza per lingua
- maggiore continuita cognitiva rispetto a una chat UI solo testuale/statica

## Test
```bash
pytest
```

## Struttura repository
```text
app/                # API, servizi, modelli, orchestrazione
alembic/            # migrazioni DB
directive/          # documenti di specifica e governance
tests/              # suite test
.github/            # CI, template issue/PR
```

## Configurazione
- Copia `.env.example` in `.env` se necessario.
- Database locale in `data/db/` (escluso da versionamento).

## Pubblicazione su GitHub checklist
1. Crea repository remoto.
2. Imposta branch di default (`main`).
3. Abilita GitHub Actions.
4. Verifica secret scanning e Dependabot (opzionale ma consigliato).
5. Push iniziale:
   ```bash
   git init
   git add .
   git commit -m "chore: bootstrap repository for github"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

## Governance e documentazione
- [CONTRIBUTING](./CONTRIBUTING.it.md)
- [SECURITY](./SECURITY.it.md)
- [CHANGELOG](./CHANGELOG.it.md)
- [Project Docs](./docs/PROJECT_OVERVIEW.it.md)
- [Ebby Mode Guide](./docs/EBBY_MODE.it.md)
- [Ebby Mode Guide (EN)](./docs/EBBY_MODE.en.md)
- [Ebby Internal Help](./docs/EBBY_INTERNAL_HELP.it.md)
- [Ebby Internal Help (EN)](./docs/EBBY_INTERNAL_HELP.en.md)

## License
[MIT](./LICENSE)

