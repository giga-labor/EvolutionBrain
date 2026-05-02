---
doc_id: evobrain-schema-api
title: EvoBrain - Schema API Definitivo
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: api
extends:
  - evobrain_costituzione_master_index.md
  - evobrain_specifica_definitiva_integrata.md
  - evobrain_ui_modalita_azione_ai.md
replaces: []
---
# EvoBrain - Schema API Definitivo
## Specifica tecnica degli endpoint, dei contratti e dei flussi applicativi

# 1. Scopo

Definire una API applicativa coerente con EvoBrain per:
- chat cognitiva
- retrieval
- gestione note e oggetti cognitivi
- progetti, task, decisioni, goal
- memoria
- simulazioni
- audit
- jobs
- configurazione runtime
- health e metacognizione

Stack consigliato:
- FastAPI
- REST JSON
- WebSocket per stream e job/event feed

Base path:
- `/api/v1`

---

# 2. Convenzioni generali

## 2.1 Formato risposta standard
```json
{
  "ok": true,
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "iso",
    "warnings": []
  },
  "error": null
}
```

## 2.2 Formato errore standard
```json
{
  "ok": false,
  "data": null,
  "meta": {
    "request_id": "uuid",
    "timestamp": "iso",
    "warnings": []
  },
  "error": {
    "code": "OBJECT_NOT_FOUND",
    "message": "Readable message",
    "details": {}
  }
}
```

## 2.3 Regole
- tutti gli endpoint mutativi devono generare audit log
- tutti gli endpoint ad alto impatto devono rispettare policy autonomia/conferma
- supportare pagination su liste
- supportare filtri coerenti
- ove utile, supportare dry-run

---

# 3. Endpoint health e stato

## GET `/health`
Risposta:
- overall_status
- db_status
- vector_status
- llm_status
- scheduler_status
- safe_mode

## GET `/system/state`
Ritorna:
- current_operational_state
- active_mode
- autonomy_level
- inference_profile
- active_project_id
- queue_depth
- last_consolidation_at

## POST `/system/safe-mode`
Body:
- enabled: bool
- reason: string

## GET `/system/config`
Configurazione runtime non sensibile.

## PATCH `/system/config`
Aggiornamento feature flags o soglie consentite.

---

# 4. Chat e reasoning

## POST `/chat/query`
Scopo: query cognitiva principale.

Body:
- session_id: string|null
- message: string
- project_id: string|null
- mode_hint: string|null
- allow_external_sources: bool default false
- inference_profile: string|null
- dry_run: bool default false

Response:
- answer
- epistemic_type
- confidence
- used_sources[]
- used_objects[]
- suggested_actions[]
- executed_actions[]
- active_mode
- context_summary

## POST `/chat/stream`
Versione streaming via SSE o WebSocket token stream.

## POST `/chat/context/add`
Aggiunge oggetti al contesto sessione.

Body:
- session_id
- items: [{object_type, object_id, context_role}]

## DELETE `/chat/context/remove`
Rimuove oggetti dal contesto.

## GET `/chat/session/{session_id}`
Dettagli sessione chat.

## POST `/chat/session`
Crea nuova sessione.

## PATCH `/chat/session/{session_id}`
Aggiorna profilo inferenziale, progetto attivo, autonomia locale.

---

# 5. Ricerca e retrieval

## GET `/search`
Parametri:
- q
- search_mode = keyword|semantic|hybrid
- object_types
- project_id
- epistemic_type
- status
- date_from
- date_to
- page
- page_size

Response:
- results[]
- facets
- query_plan
- total

## POST `/search/advanced`
Body JSON strutturato con filtri complessi.

## POST `/search/compare`
Confronta più oggetti.

Body:
- items: [{object_type, object_id}]
- compare_mode: semantic|structural|project|timeline

Response:
- comparison_summary
- similarities[]
- differences[]
- conflicts[]
- recommended_links[]

## GET `/search/suggestions`
Suggerimenti autocomplete e oggetti vicini.

---

# 6. Note e documenti

## POST `/documents/import`
Body:
- source_type
- source_uri|null
- content|null
- title|null
- project_id|null
- metadata|null

Response:
- document_id
- job_id
- ingestion_status

## POST `/documents/import/file`
Upload file multipart.

## GET `/documents`
Lista documenti.

## GET `/documents/{document_id}`
Dettaglio documento.

## GET `/documents/{document_id}/chunks`
Lista chunk.

## POST `/documents/{document_id}/reprocess`
Rilancia pipeline.

Body:
- stages: [normalization, semantic, knowledge]

## POST `/notes`
Crea nota.

Body:
- title
- body_markdown
- note_type
- project_id|null
- tags|null
- epistemic_type

## GET `/notes`
Lista note con filtri.

## GET `/notes/{note_id}`
Dettaglio nota.

## PATCH `/notes/{note_id}`
Aggiorna nota.

Supportare:
- title
- body_markdown
- status
- tags
- project_id

## DELETE `/notes/{note_id}`
Soft delete, con conferma forte se nota strategica.

## GET `/notes/{note_id}/versions`
Storico versioni.

---

# 7. Concetti, entità e relazioni

## GET `/concepts`
Lista concetti.

## POST `/concepts`
Crea concetto manuale o assistito.

## GET `/concepts/{concept_id}`
Dettaglio concetto.

## PATCH `/concepts/{concept_id}`
Aggiorna.

## POST `/concepts/{concept_id}/merge`
Merge concetti.

Body:
- target_concept_id
- dry_run: bool
- confirmation_token|null

Response:
- merge_plan
- impacted_objects[]
- requires_confirmation

## GET `/entities`
Lista entità.

## GET `/relations`
Lista relazioni filtrabili.

Parametri:
- source_object_type
- source_object_id
- target_object_type
- target_object_id
- relation_type
- validation_status

## POST `/relations`
Crea relazione.

## PATCH `/relations/{relation_id}`
Aggiorna confidence, validation_status, metadata.

## DELETE `/relations/{relation_id}`
Soft delete.

---

# 8. Progetti, goal, task, decisioni

## GET `/projects`
## POST `/projects`
## GET `/projects/{project_id}`
## PATCH `/projects/{project_id}`
## DELETE `/projects/{project_id}`

## GET `/projects/{project_id}/workspace`
Response unificata:
- project
- goals
- tasks
- decisions
- recent_notes
- top_concepts
- blockers
- timeline

## GET `/goals`
## POST `/goals`
## GET `/goals/{goal_id}`
## PATCH `/goals/{goal_id}`

## GET `/tasks`
## POST `/tasks`
## GET `/tasks/{task_id}`
## PATCH `/tasks/{task_id}`
## DELETE `/tasks/{task_id}`

## GET `/decisions`
## POST `/decisions`
## GET `/decisions/{decision_id}`
## PATCH `/decisions/{decision_id}`

## POST `/decisions/{decision_id}/review`
Registra revisione esito.

---

# 9. Memoria

## GET `/memory/items`
Filtri:
- memory_layer
- object_type
- project_id
- min_score
- status

## GET `/memory/items/{memory_item_id}`
## POST `/memory/recalculate`
Ricalcola punteggi.

Body:
- scope: all|project|object
- project_id|null
- object_type|null
- object_id|null

## POST `/memory/promote`
Body:
- object_type
- object_id
- target_layer
- reason
- dry_run

## POST `/memory/demote`
Analogous.

## GET `/memory/events`
Storico memory events.

## GET `/memory/dashboard`
Response:
- active_items
- rising_items
- decaying_items
- recent_promotions
- recent_demotions
- conflicts
- pending_validation

---

# 10. Episodi, procedure e scenari

## GET `/episodes`
## POST `/episodes`
## GET `/episodes/{episode_id}`
## PATCH `/episodes/{episode_id}`

## GET `/procedures`
## POST `/procedures`
## GET `/procedures/{procedure_id}`
## PATCH `/procedures/{procedure_id}`

## GET `/scenarios`
## POST `/scenarios`
Crea scenario.

Body:
- title
- description
- scenario_type
- premise
- assumptions
- project_id|null
- dry_run

## POST `/scenarios/{scenario_id}/simulate`
Body:
- inference_profile
- model_hint|null

Response:
- outputs
- limitations
- confidence
- conflicts

## GET `/scenarios/{scenario_id}`

---

# 11. Feedback e adattamento

## POST `/feedback`
Body:
- target_object_type
- target_object_id
- feedback_type
- score_delta|null
- free_text|null
- session_id|null

## GET `/feedback`
Filtrabile per target e utente.

## POST `/adaptation/recalibrate`
Avvia job di ricalibrazione.

## GET `/adaptation/status`
Ritorna:
- adaptation_profile
- recent_updates
- drift_flags
- ranking_changes

## GET `/self-model`
## PATCH `/self-model`
Campi limitati e con conferma per cambi critici.

## GET `/user-model`
## PATCH `/user-model`

---

# 12. Audit, jobs e rollback

## GET `/audit/logs`
Filtri:
- event_type
- module_name
- action_type
- target_object_type
- target_object_id
- date_from/date_to

## GET `/audit/logs/{audit_id}`

## GET `/jobs`
## POST `/jobs`
Crea job manuale.

Body:
- job_type
- payload
- priority|null
- scheduled_for|null

## GET `/jobs/{job_id}`
## POST `/jobs/{job_id}/cancel`
## POST `/jobs/{job_id}/retry`

## GET `/rollbacks`
## POST `/rollbacks`
Crea rollback point manuale.

## POST `/rollbacks/{rollback_id}/restore`
Richiede conferma forte.

---

# 13. Dashboard specialistiche

## GET `/dashboard/metacognition`
- retrieval_quality
- context_sufficiency
- overconfidence_risk
- fallback_count
- drift_signals

## GET `/dashboard/self`
- self_model summary
- autonomy_level
- active_capabilities
- current_focus
- recent_failures
- recent_successes

## GET `/dashboard/review/daily`
## GET `/dashboard/review/weekly`

---

# 14. WebSocket / Event stream

## WS `/ws/events`
Eventi:
- job_updated
- audit_created
- system_state_changed
- memory_promoted
- memory_demoted
- conflict_detected
- safe_mode_changed

## WS `/ws/chat/{session_id}`
Per token stream e interazione real-time.

---

# 15. Sicurezza e permessi logici

Livelli minimi:
- read
- write_low
- write_medium
- write_high
- admin_runtime

Azioni che richiedono conferma forte:
- merge concetti
- promozione strategica
- declassamento strategico
- cancellazioni importanti
- restore rollback
- modifica self-model ad alto impatto
- reset scoring massivo

Supportare:
- dry_run
- confirmation_token
- audit mandatory

---

# 16. Codici errore principali

- OBJECT_NOT_FOUND
- VALIDATION_ERROR
- PERMISSION_DENIED
- CONFIRMATION_REQUIRED
- CONFLICT_DETECTED
- SAFE_MODE_RESTRICTION
- JOB_NOT_RUNNABLE
- EXTERNAL_SOURCE_DISABLED
- CONTEXT_INSUFFICIENT
- INTEGRITY_ERROR
- PROVIDER_UNAVAILABLE

---

# 17. Definition of Done

Questa API è completa se:
1. copre tutte le capacità principali di EvoBrain
2. separa read, action e admin runtime
3. supporta chat, retrieval, memoria, progetti, audit e jobs
4. supporta stream eventi
5. gestisce conferme e dry-run
6. impone audit su mutazioni rilevanti
