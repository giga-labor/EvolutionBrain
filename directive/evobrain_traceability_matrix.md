---
doc_id: evobrain-traceability-matrix
title: EvoBrain - Traceability Matrix
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: governance
extends:
  - evobrain_specifica_definitiva_integrata.md
  - evobrain_roadmap_implementativa.md
  - evobrain_schema_database.md
  - evobrain_schema_api.md
  - evobrain_test_plan.md
replaces: []
---

# EvoBrain - Traceability Matrix

## Scopo

Questo file collega ogni requisito implementativo a:
- documento sorgente
- modulo responsabile
- tabella DB
- endpoint API
- test
- fase roadmap
- stato di implementazione

Regola: nessun requisito puo essere considerato "done" se non e tracciato qui con evidenza verificabile.

## Stati consentiti

- `not_started`
- `in_progress`
- `implemented_unverified`
- `verified`
- `blocked`
- `deprecated`

## Matrice principale

| req_id | requirement | source_doc | source_section | module_owner | db_table | api_endpoint | test_id | roadmap_phase | impl_status | evidence_ref | updated_at | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-ING-001 | Import text/file con deduplica hash | evobrain_specifica_definitiva_integrata.md | 24.1 Pipeline di ingestione | ingestion | documents, jobs | POST /api/v1/documents/import | T-ING-001 | 1 | verified | tests/test_documents.py | 2026-04-27 | ingestione testo + deduplica hash attiva |
| REQ-RET-001 | Hybrid retrieval (keyword + semantic) | evobrain_specifica_definitiva_integrata.md | 5.3, 23, 24 | semantic, reasoning | documents, notes, concepts | GET /api/v1/search | T-RET-001 | 2 | verified | tests/test_search_chat.py | 2026-04-27 | mode keyword/semantic/hybrid operativo |
| REQ-KNW-001 | Gestione concepts/entities/relations | evobrain_specifica_definitiva_integrata.md | 20, 24.2 | knowledge | concepts, relations | /api/v1/concepts/*, /api/v1/relations/* | T-KNW-001 | 3 | verified | tests/test_phase_closure_features.py | 2026-04-27 | concepts + relations CRUD operativo |
| REQ-PRJ-001 | CRUD reale projects/goals/tasks/decisions | evobrain_roadmap_implementativa.md | Fase 3 | projects | projects, goals, tasks, decisions | /api/v1/projects/*, /api/v1/goals/*, /api/v1/tasks/*, /api/v1/decisions/* | T-PRJ-001 | 3 | verified | tests/test_phase_closure_features.py | 2026-04-27 | workflow completo attivo |
| REQ-MEM-001 | Memory scoring + promotion/demotion | evobrain_specifica_definitiva_integrata.md | 25, 26 | memory | memory_items | POST /api/v1/memory/recalculate | T-MEM-001 | 4 | verified | tests/test_cognitive_structures.py | 2026-04-27 | scoring e ricalcolo operativi |
| REQ-ATT-001 | Attention engine operativo | evobrain_specifica_definitiva_integrata.md | 10 | attention | memory_items | POST /api/v1/attention/focus | T-ATT-001 | 5 | verified | tests/test_phase_closure_features.py | 2026-04-27 | focus selection attiva e usata in reasoning |
| REQ-EPI-001 | Episodic memory persistente | evobrain_specifica_definitiva_integrata.md | 9.9 | memory | episodes | /api/v1/episodes/* | T-EPI-001 | 5 | verified | tests/test_phase_closure_features.py | 2026-04-27 | CRUD episodi operativo |
| REQ-PROC-001 | Procedural memory persistente | evobrain_specifica_definitiva_integrata.md | 9.10 | memory | procedures | /api/v1/procedures/* | T-PROC-001 | 5 | verified | tests/test_phase_closure_features.py | 2026-04-27 | CRUD procedure operativo |
| REQ-SLF-001 | Self model operativo | evobrain_specifica_definitiva_integrata.md | 6 | identity | self_model | GET/PUT /api/v1/self-model | T-SLF-001 | 5 | verified | tests/test_phase_closure_features.py | 2026-04-27 | singleton self model aggiornabile |
| REQ-META-001 | Metacognitive monitor | evobrain_specifica_definitiva_integrata.md | 12 | metacognition | system_state | POST /api/v1/meta/evaluate | T-META-001 | 6 | verified | tests/test_phase_closure_features.py | 2026-04-27 | metacognition in loop reasoning + endpoint |
| REQ-DRF-001 | Drift detection + contradiction scan | evobrain_specifica_definitiva_integrata.md | 14, 36 | semantic, metacognition | relations, audit_entries | POST /api/v1/maintenance/contradictions | T-DRF-001 | 6 | verified | tests/test_phase_closure_features.py | 2026-04-27 | scan e report con audit/job |
| REQ-UI-001 | Dashboard e audit console live | evobrain_ui_modalita_azione_ai.md | 4, 19 | ui | audit_entries, documents, notes, projects | GET /api/v1/ui/dashboard, GET /api/v1/ui/audit | T-UI-001 | 8 | verified | tests/test_phase_closure_features.py | 2026-04-27 | UI HTML con fetch live su API |
| REQ-AUD-001 | Audit log mutazioni obbligatorio | evobrain_costituzione_master_index.md | 17 | audit | audit_entries | GET /api/v1/audit/logs | T-AUD-001 | 0 | verified | tests/test_cognitive_structures.py | 2026-04-27 | endpoint audit operativo e popolato |
| REQ-SAF-001 | Safe mode + rollback + backup | evobrain_specifica_definitiva_integrata.md | 29, 30 | safety, scheduler | system_state, jobs | POST /api/v1/system/safe-mode | T-SAF-001 | 7 | verified | tests/test_phase_closure_features.py | 2026-04-27 | safe mode middleware + backup/restore validati |

## Vista copertura per fase

| roadmap_phase | requisiti_totali | verified | coverage_pct | blocker_count | owner |
|---|---:|---:|---:|---:|---|
| 0 | 1 | 1 | 100 | 0 | core |
| 1 | 1 | 1 | 100 | 0 | ingestion |
| 2 | 1 | 1 | 100 | 0 | semantic |
| 3 | 2 | 2 | 100 | 0 | knowledge/projects |
| 4 | 1 | 1 | 100 | 0 | memory |
| 5 | 4 | 4 | 100 | 0 | cognitive |
| 6 | 2 | 2 | 100 | 0 | metacognition |
| 7 | 1 | 1 | 100 | 0 | safety |
| 8 | 1 | 1 | 100 | 0 | ui |

## Regole di mantenimento

1. Ogni nuova feature deve introdurre almeno una riga `REQ-*` in questa matrice.
2. Ogni PR che cambia comportamento deve aggiornare `impl_status`, `evidence_ref` e `updated_at`.
3. `impl_status=verified` e consentito solo con `test_id` passato e `evidence_ref` compilato.
4. Se un requisito cambia, non si sovrascrive `req_id`: si crea nuova riga e si marca la precedente `deprecated`.

## Template riga nuova

| req_id | requirement | source_doc | source_section | module_owner | db_table | api_endpoint | test_id | roadmap_phase | impl_status | evidence_ref | updated_at | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-XXX-000 |  |  |  |  |  |  |  |  | not_started |  |  |  |
