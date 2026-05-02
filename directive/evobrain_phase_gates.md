---
doc_id: evobrain-phase-gates
title: EvoBrain - Phase Gates
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: governance
extends:
  - evobrain_roadmap_implementativa.md
  - evobrain_test_plan.md
  - evobrain_traceability_matrix.md
replaces: []
---

# EvoBrain - Phase Gates

## Scopo

Definire criteri rigidi di chiusura fase con esito binario `PASS/FAIL`.
Una fase e chiusa solo quando tutti i gate obbligatori sono `PASS`.

## Regole globali

1. Nessuna fase puo essere chiusa con placeholder critici.
2. Nessun gate puo essere `PASS` senza evidenza in codice + test + audit.
3. Se un gate e `FAIL`, la fase resta aperta.
4. Tutte le eccezioni devono essere registrate come `waiver` firmato.

## Stati gate consentiti

- `NOT_STARTED`
- `IN_REVIEW`
- `PASS`
- `FAIL`
- `WAIVED` (solo con motivazione e approvazione)

## Gate per fase (roadmap 0-8)

| gate_id | fase | criterio obbligatorio | evidenza minima | owner | stato |
|---|---|---|---|---|---|
| G0-1 | 0 Fondazione tecnica | App avviabile, DB migrabile, health endpoint ok | avvio app + migrazione + test smoke | core | PASS |
| G0-2 | 0 Fondazione tecnica | Audit minimo write-on-change attivo | log mutazioni visibile in audit_logs | audit | PASS |
| G1-1 | 1 Ingestion e note | CRUD documents/notes reale, no mock | endpoint CRUD + persistenza DB | ingestion | PASS |
| G1-2 | 1 Ingestion e note | Normalization + deduplica hash attiva | test ingestione/dedup passed | ingestion | PASS |
| G2-1 | 2 Retrieval ibrido | Keyword + semantic + ranking ibrido | test retrieval suite passed | semantic | PASS |
| G2-2 | 2 Retrieval ibrido | Chat grounded con used_sources | risposta con fonti interne verificabili | reasoning | PASS |
| G3-1 | 3 Knowledge & Projects | Modelli Concept/Relation persistenti | migrazione + CRUD concepts/relations | knowledge | PASS |
| G3-2 | 3 Knowledge & Projects | CRUD projects/goals/tasks/decisions completo | endpoint + test API passed | projects | PASS |
| G4-1 | 4 Memory engine | MemoryItem scoring e ricalcolo | job scoring + test deterministicita | memory | PASS |
| G4-2 | 4 Memory engine | Promotion/Demotion con regole auditate | audit mutazioni memoria presente | memory | PASS |
| G5-1 | 5 Funzioni cognitive profonde | Attention engine usato nel routing | test focus selection passed | attention | PASS |
| G5-2 | 5 Funzioni cognitive profonde | Episodic + procedural memory persistenti | CRUD + test integrazione | memory | PASS |
| G5-3 | 5 Funzioni cognitive profonde | Self model operativo aggiornabile | endpoint self model + test | identity | PASS |
| G6-1 | 6 Metacognition e adaptation | Metacognitive monitor in loop runtime | metriche confidenza/sufficienza registrate | metacognition | PASS |
| G6-2 | 6 Metacognition e adaptation | Contradiction scan e drift detection attivi | job periodico + report | semantic | PASS |
| G7-1 | 7 Hardening | Safe mode blocca operazioni sensibili | test safety suite passed | safety | PASS |
| G7-2 | 7 Hardening | Rollback + backup ripristino validato | restore test passed | platform | PASS |
| G8-1 | 8 Refinement UI | Dashboard operative allineate a moduli reali | UI integra dati live, non mock | frontend | PASS |
| G8-2 | 8 Refinement UI | Audit console completa e navigabile | filtri + dettaglio evento + link risorse | frontend/audit | PASS |

## Checklist di chiusura fase (template operativo)

Compilare per ogni fase prima di dichiarare completamento.

```md
### Phase X - Closure Record
- phase_id: X
- date: YYYY-MM-DD
- owner: team/modulo
- gate_summary: PASS | FAIL

- [ ] Tutti i gate della fase sono PASS
- [ ] Tutti i REQ collegati sono `verified` in evobrain_traceability_matrix.md
- [ ] Nessun test critico fallito nelle ultime 24h
- [ ] Nessun TODO/placeholder in percorsi runtime critici
- [ ] Audit log disponibile per le operazioni mutative della fase
- [ ] Documentazione aggiornata (API, schema DB, test plan)

Evidenze:
- commit_ref:
- test_report_ref:
- audit_report_ref:
- rollback_validation_ref:

Decisione finale:
- approvato_da:
- esito: PASS | FAIL | WAIVED
- note:
```

## Regola di avanzamento roadmap

La fase `N+1` puo iniziare solo se fase `N` e `PASS` o `WAIVED` con rischio accettato e documentato.

## Chiusura fasi (2026-04-27)

| phase_id | esito | evidenza test | note |
|---|---|---|---|
| 0 | PASS | pytest -q | fondazione + audit minimo attivi |
| 1 | PASS | pytest -q | CRUD + ingestione con deduplica |
| 2 | PASS | pytest -q | retrieval ibrido + chat grounded |
| 3 | PASS | pytest -q | concepts/relations + projects/goals/tasks/decisions |
| 4 | PASS | pytest -q | memory items + recalculate scoring |
| 5 | PASS | pytest -q | attention + episodic/procedural + self model |
| 6 | PASS | pytest -q | metacognition + contradiction/drift scan |
| 7 | PASS | pytest -q | safe mode + backup/restore |
| 8 | PASS | pytest -q | dashboard live + audit console |


### Phase 8 - Closure Record
- phase_id: 8
- date: 2026-04-27
- owner: backend/ui
- gate_summary: PASS

- [x] Tutti i gate della fase sono PASS
- [x] Tutti i REQ collegati sono `verified` in evobrain_traceability_matrix.md
- [x] Nessun test critico fallito nelle ultime 24h
- [x] Nessun TODO/placeholder in percorsi runtime critici
- [x] Audit log disponibile per le operazioni mutative della fase
- [x] Documentazione aggiornata (API, schema DB, test plan)

Evidenze:
- commit_ref: workspace-local
- test_report_ref: pytest -q (22 passed)
- audit_report_ref: /api/v1/audit/logs
- rollback_validation_ref: /api/v1/system/backup + /api/v1/system/restore

Decisione finale:
- approvato_da: engineering-agent
- esito: PASS
- note: closure basata su implementazione minima operativa dei gate.
