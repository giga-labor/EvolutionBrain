# Project Overview

## Visione
EvoBrain Zero punta a fornire una base locale, modulare e auditabile per memoria, ragionamento assistito e operativita su conoscenza strutturata.

## Moduli principali
- `app/api`: routing HTTP
- `app/db`: modelli SQLAlchemy e repository
- `app/reasoning`: orchestrazione chat e reasoning
- `app/ingestion`: import e pipeline documenti
- `app/memory`: gestione layer memoria
- `app/audit`: tracciamento eventi

## Dati
- DB SQLite locale (`data/db/evobrain.db`)
- Migrazioni in `alembic/versions`

## Canali di interazione
Il progetto supporta due canali principali:

1. **Interfaccia agentica/IDE (raccomandata)**
- migliore per sviluppo, manutenzione e iterazione con LLM
- consente lettura/scrittura multi-file, esecuzione test e debug continuo
- sfrutta pienamente la modularita del progetto (API, DB, servizi, directive, test)

2. **Chat UI**
- utile per uso operativo rapido e comandi diretti
- valida per esplorazione e interazioni brevi
- con limiti strutturali su modifiche estese, verifica profonda e cicli complessi di sviluppo

Decisione pratica: per evoluzione del sistema e quality loop continuo, privilegiare il canale agentico in IDE; usare la Chat UI come superficie operativa leggera.

## Layer concettuale vs layer linguistico
Nel modello operativo EvoBrain:
- la memoria consolidata mantiene **concetti** e relazioni (indipendenti dalla lingua)
- l'LLM realizza la **resa linguistica** in base alla lingua e al registro dell'utente

Questo e un vantaggio strutturale del canale LLM: la conoscenza resta unificata, mentre l'espressione si adatta dinamicamente.

## Attivazione della voce Ebby
Nelle sessioni LLM e raccomandato un handshake iniziale esplicito:
- lettura dei documenti guida (`directive/`)
- dichiarazione identita (`Ebby`) e ruolo (secondo cervello operativo)
- impostazione policy operative e limiti
- conferma sintetica dell'attivazione

Riferimento operativo: [docs/EBBY_MODE.it.md](./EBBY_MODE.it.md)

## Test strategy
- test endpoint principali
- test moduli cognitivi
- test servizi operativi
- test regressione integrazioni base

## Deployment baseline
- avvio con `uvicorn app.main:app --reload`
- CI GitHub Actions per test automatici

## Roadmap minima suggerita
1. hardening configurazione e segreti
2. coverage test + quality gates
3. packaging release/tag
4. documentazione API OpenAPI dedicata
