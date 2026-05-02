---
doc_id: evobrain-schema-database
title: EvoBrain - Schema Database Definitivo
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: data
extends:
  - evobrain_costituzione_master_index.md
  - evobrain_specifica_definitiva_integrata.md
replaces: []
---
# EvoBrain - Schema Database Definitivo
## Specifica tecnica completa del database relazionale principale

# 1. Scopo

Definire lo schema relazionale definitivo di EvoBrain, comprensivo di:
- tabelle principali
- chiavi primarie e foreign key
- indici
- vincoli
- stati
- campi di audit
- pattern di versionamento
- supporto a memoria, conoscenza, azioni, feedback, audit e runtime

Database iniziale target:
- SQLite per sviluppo e uso locale
- compatibile con PostgreSQL per produzione o crescita

---

# 2. Convenzioni generali

## 2.1 Tipi logici
- `id`: UUID string
- `created_at`: timestamp ISO o datetime DB
- `updated_at`: timestamp ISO o datetime DB
- `deleted_at`: nullable timestamp per soft delete
- `status`: string enum controllata a livello app
- `json_data`: JSON/TEXT serializzato
- `confidence`: float 0.0–1.0
- `score`: float
- `version`: integer >= 1

## 2.2 Regole
- ogni tabella persistente deve avere `id`, `created_at`, `updated_at`
- niente hard delete per oggetti cognitivi centrali
- gli oggetti principali usano soft delete
- relazioni critiche devono avere `confidence` e `origin`
- ogni modifica importante deve generare audit log separato

---

# 3. Tabelle core sorgente e contenuto

## 3.1 `documents`
Rappresenta il documento sorgente logico.

Campi:
- id TEXT PK
- source_type TEXT NOT NULL
- source_uri TEXT NULL
- source_label TEXT NULL
- title TEXT NULL
- content_hash TEXT NOT NULL
- mime_type TEXT NULL
- language TEXT NULL
- size_bytes INTEGER NULL
- ingestion_status TEXT NOT NULL
- normalization_status TEXT NOT NULL
- semantic_status TEXT NOT NULL
- validation_status TEXT NOT NULL
- project_id TEXT NULL FK -> projects.id
- root_note_id TEXT NULL FK -> notes.id
- raw_path TEXT NULL
- normalized_path TEXT NULL
- metadata_json TEXT NULL
- quality_score REAL DEFAULT 0
- confidence REAL DEFAULT 1
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_documents_hash(content_hash)
- idx_documents_project(project_id)
- idx_documents_source_type(source_type)
- idx_documents_ingestion_status(ingestion_status)

Vincoli:
- UNIQUE(content_hash, source_uri)

## 3.2 `document_versions`
Versioni storiche del documento.

Campi:
- id TEXT PK
- document_id TEXT NOT NULL FK -> documents.id
- version INTEGER NOT NULL
- content_hash TEXT NOT NULL
- title TEXT NULL
- raw_path TEXT NULL
- normalized_path TEXT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL

Vincoli:
- UNIQUE(document_id, version)

## 3.3 `chunks`
Unità minime di testo indicizzabile e recuperabile.

Campi:
- id TEXT PK
- document_id TEXT NOT NULL FK -> documents.id
- chunk_index INTEGER NOT NULL
- chunk_type TEXT NOT NULL
- title TEXT NULL
- content TEXT NOT NULL
- token_estimate INTEGER NULL
- char_count INTEGER NULL
- start_offset INTEGER NULL
- end_offset INTEGER NULL
- semantic_status TEXT NOT NULL
- lexical_status TEXT NOT NULL
- quality_score REAL DEFAULT 0
- confidence REAL DEFAULT 1
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Vincoli:
- UNIQUE(document_id, chunk_index)

Indici:
- idx_chunks_document(document_id)
- idx_chunks_semantic_status(semantic_status)

---

# 4. Tabelle note e contenuti human-readable

## 4.1 `notes`
Nota logica principale leggibile da utente.

Campi:
- id TEXT PK
- document_id TEXT NULL FK -> documents.id
- note_type TEXT NOT NULL
- title TEXT NOT NULL
- slug TEXT NULL
- body_markdown TEXT NOT NULL
- summary TEXT NULL
- source_type TEXT NOT NULL
- project_id TEXT NULL FK -> projects.id
- parent_note_id TEXT NULL FK -> notes.id
- status TEXT NOT NULL
- epistemic_type TEXT NOT NULL
- confidence REAL DEFAULT 1
- relevance_score REAL DEFAULT 0
- strategic_weight REAL DEFAULT 0
- tags_json TEXT NULL
- metadata_json TEXT NULL
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_notes_project(project_id)
- idx_notes_type(note_type)
- idx_notes_status(status)
- idx_notes_relevance(relevance_score)

## 4.2 `note_versions`
Storico revisioni nota.

Campi:
- id TEXT PK
- note_id TEXT NOT NULL FK -> notes.id
- version INTEGER NOT NULL
- title TEXT NOT NULL
- body_markdown TEXT NOT NULL
- summary TEXT NULL
- change_reason TEXT NULL
- changed_by TEXT NOT NULL
- created_at TEXT NOT NULL

Vincoli:
- UNIQUE(note_id, version)

---

# 5. Tabelle conoscenza strutturata

## 5.1 `concepts`
Concetti persistenti.

Campi:
- id TEXT PK
- canonical_label TEXT NOT NULL
- description TEXT NULL
- concept_type TEXT NOT NULL
- status TEXT NOT NULL
- epistemic_type TEXT NOT NULL
- confidence REAL DEFAULT 0.5
- relevance_score REAL DEFAULT 0
- strategic_weight REAL DEFAULT 0
- semantic_centrality_score REAL DEFAULT 0
- link_density_score REAL DEFAULT 0
- project_id TEXT NULL FK -> projects.id
- origin TEXT NOT NULL
- metadata_json TEXT NULL
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_concepts_label(canonical_label)
- idx_concepts_project(project_id)
- idx_concepts_status(status)

## 5.2 `entities`
Entità nominate generiche.

Campi:
- id TEXT PK
- name TEXT NOT NULL
- entity_type TEXT NOT NULL
- canonical_form TEXT NULL
- description TEXT NULL
- confidence REAL DEFAULT 0.5
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Indici:
- idx_entities_name(name)
- idx_entities_type(entity_type)

## 5.3 `relations`
Relazioni tra oggetti cognitivi.

Campi:
- id TEXT PK
- source_object_type TEXT NOT NULL
- source_object_id TEXT NOT NULL
- target_object_type TEXT NOT NULL
- target_object_id TEXT NOT NULL
- relation_type TEXT NOT NULL
- directionality TEXT NOT NULL
- confidence REAL DEFAULT 0.5
- validation_status TEXT NOT NULL
- origin TEXT NOT NULL
- evidence_json TEXT NULL
- metadata_json TEXT NULL
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_relations_source(source_object_type, source_object_id)
- idx_relations_target(target_object_type, target_object_id)
- idx_relations_type(relation_type)
- idx_relations_validation(validation_status)

## 5.4 `evidence`
Evidenze legate a fatti, inferenze o decisioni.

Campi:
- id TEXT PK
- evidence_type TEXT NOT NULL
- title TEXT NULL
- description TEXT NULL
- source_object_type TEXT NOT NULL
- source_object_id TEXT NOT NULL
- strength_score REAL DEFAULT 0
- confidence REAL DEFAULT 1
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

## 5.5 `hypotheses`
Ipotesi esplicite.

Campi:
- id TEXT PK
- title TEXT NOT NULL
- description TEXT NOT NULL
- status TEXT NOT NULL
- confidence REAL DEFAULT 0.2
- project_id TEXT NULL FK -> projects.id
- support_score REAL DEFAULT 0
- conflict_score REAL DEFAULT 0
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

## 5.6 `scenarios`
Scenari simulativi.

Campi:
- id TEXT PK
- title TEXT NOT NULL
- description TEXT NOT NULL
- scenario_type TEXT NOT NULL
- premise_json TEXT NOT NULL
- assumptions_json TEXT NULL
- outputs_json TEXT NULL
- risk_score REAL DEFAULT 0
- confidence REAL DEFAULT 0.3
- project_id TEXT NULL FK -> projects.id
- status TEXT NOT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

---

# 6. Tabelle progetto, obiettivi, decisioni e task

## 6.1 `projects`
Campi:
- id TEXT PK
- name TEXT NOT NULL
- slug TEXT NULL
- description TEXT NULL
- project_type TEXT NOT NULL
- status TEXT NOT NULL
- priority REAL DEFAULT 0
- urgency REAL DEFAULT 0
- strategic_weight REAL DEFAULT 0
- active_goal_id TEXT NULL
- owner_type TEXT NOT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_projects_status(status)
- idx_projects_priority(priority)

## 6.2 `goals`
Campi:
- id TEXT PK
- project_id TEXT NULL FK -> projects.id
- goal_type TEXT NOT NULL
- title TEXT NOT NULL
- description TEXT NULL
- owner_type TEXT NOT NULL
- owner_id TEXT NULL
- status TEXT NOT NULL
- priority REAL DEFAULT 0
- urgency REAL DEFAULT 0
- strategic_weight REAL DEFAULT 0
- due_window_start TEXT NULL
- due_window_end TEXT NULL
- confidence REAL DEFAULT 0.8
- risk_level TEXT NOT NULL
- dependencies_json TEXT NULL
- blockers_json TEXT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Indici:
- idx_goals_project(project_id)
- idx_goals_status(status)
- idx_goals_priority(priority, urgency)

## 6.3 `tasks`
Campi:
- id TEXT PK
- project_id TEXT NULL FK -> projects.id
- goal_id TEXT NULL FK -> goals.id
- title TEXT NOT NULL
- description TEXT NULL
- task_type TEXT NOT NULL
- status TEXT NOT NULL
- priority REAL DEFAULT 0
- urgency REAL DEFAULT 0
- assignee_type TEXT NOT NULL
- assignee_id TEXT NULL
- due_at TEXT NULL
- started_at TEXT NULL
- completed_at TEXT NULL
- confidence REAL DEFAULT 0.8
- source_object_type TEXT NULL
- source_object_id TEXT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL
- deleted_at TEXT NULL

Indici:
- idx_tasks_project(project_id)
- idx_tasks_goal(goal_id)
- idx_tasks_status(status)
- idx_tasks_due(due_at)

## 6.4 `decisions`
Campi:
- id TEXT PK
- project_id TEXT NULL FK -> projects.id
- goal_id TEXT NULL FK -> goals.id
- title TEXT NOT NULL
- description TEXT NOT NULL
- context_summary TEXT NULL
- status TEXT NOT NULL
- decision_type TEXT NOT NULL
- confidence REAL DEFAULT 0.6
- risk_level TEXT NOT NULL
- rationale_json TEXT NULL
- alternatives_json TEXT NULL
- expected_outcomes_json TEXT NULL
- review_due_at TEXT NULL
- decided_at TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Indici:
- idx_decisions_project(project_id)
- idx_decisions_status(status)
- idx_decisions_review_due(review_due_at)

---

# 7. Tabelle memoria evolutiva

## 7.1 `memory_items`
Rappresenta un item in uno dei layer di memoria.

Campi:
- id TEXT PK
- object_type TEXT NOT NULL
- object_id TEXT NOT NULL
- memory_layer TEXT NOT NULL
- status TEXT NOT NULL
- memory_score REAL DEFAULT 0
- recency_score REAL DEFAULT 0
- frequency_score REAL DEFAULT 0
- user_interest_score REAL DEFAULT 0
- project_relevance_score REAL DEFAULT 0
- strategic_weight REAL DEFAULT 0
- semantic_centrality_score REAL DEFAULT 0
- link_density_score REAL DEFAULT 0
- validation_score REAL DEFAULT 0
- uncertainty_penalty REAL DEFAULT 0
- episodic_reinforcement_score REAL DEFAULT 0
- procedural_utility_score REAL DEFAULT 0
- decay_factor REAL DEFAULT 1
- promoted_from TEXT NULL
- demoted_from TEXT NULL
- last_accessed_at TEXT NULL
- last_scored_at TEXT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Vincoli:
- UNIQUE(object_type, object_id, memory_layer)

Indici:
- idx_memory_items_layer(memory_layer)
- idx_memory_items_score(memory_score DESC)
- idx_memory_items_last_accessed(last_accessed_at)

## 7.2 `memory_events`
Eventi di promozione/declassamento/accesso.

Campi:
- id TEXT PK
- memory_item_id TEXT NOT NULL FK -> memory_items.id
- event_type TEXT NOT NULL
- old_layer TEXT NULL
- new_layer TEXT NULL
- old_score REAL NULL
- new_score REAL NULL
- reason TEXT NULL
- actor_type TEXT NOT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL

---

# 8. Memoria episodica e procedurale

## 8.1 `episodes`
Campi:
- id TEXT PK
- title TEXT NOT NULL
- description TEXT NULL
- episode_type TEXT NOT NULL
- context_json TEXT NULL
- actors_json TEXT NULL
- trigger_json TEXT NULL
- actions_json TEXT NULL
- outcomes_json TEXT NULL
- lessons_json TEXT NULL
- impact_score REAL DEFAULT 0
- confidence REAL DEFAULT 0.8
- project_id TEXT NULL FK -> projects.id
- started_at TEXT NULL
- ended_at TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

## 8.2 `procedures`
Campi:
- id TEXT PK
- title TEXT NOT NULL
- description TEXT NULL
- procedure_type TEXT NOT NULL
- steps_json TEXT NOT NULL
- prerequisites_json TEXT NULL
- expected_outputs_json TEXT NULL
- success_criteria_json TEXT NULL
- failure_modes_json TEXT NULL
- utility_score REAL DEFAULT 0
- confidence REAL DEFAULT 0.7
- status TEXT NOT NULL
- project_id TEXT NULL FK -> projects.id
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

---

# 9. Modelli identitari e adattivi

## 9.1 `user_model`
Campi:
- id TEXT PK
- user_key TEXT NOT NULL
- preferences_json TEXT NULL
- style_profile_json TEXT NULL
- dominant_projects_json TEXT NULL
- response_preferences_json TEXT NULL
- query_patterns_json TEXT NULL
- decision_patterns_json TEXT NULL
- constraints_json TEXT NULL
- adaptation_profile_json TEXT NULL
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Vincoli:
- UNIQUE(user_key)

## 9.2 `self_model`
Campi:
- id TEXT PK
- self_name TEXT NOT NULL
- self_role TEXT NOT NULL
- mission_profile_json TEXT NULL
- active_capabilities_json TEXT NULL
- disabled_capabilities_json TEXT NULL
- risk_tolerance_profile_json TEXT NULL
- autonomy_level TEXT NOT NULL
- trust_profile_json TEXT NULL
- known_limits_json TEXT NULL
- current_operational_state TEXT NOT NULL
- current_focus_json TEXT NULL
- current_load REAL DEFAULT 0
- current_confidence REAL DEFAULT 0.5
- recent_failures_json TEXT NULL
- recent_successes_json TEXT NULL
- adaptation_state_json TEXT NULL
- version INTEGER NOT NULL DEFAULT 1
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

---

# 10. Embeddings e semantica

## 10.1 `embeddings_registry`
Registro degli embedding generati.

Campi:
- id TEXT PK
- object_type TEXT NOT NULL
- object_id TEXT NOT NULL
- embedding_provider TEXT NOT NULL
- embedding_model TEXT NOT NULL
- embedding_dim INTEGER NOT NULL
- vector_ref TEXT NOT NULL
- content_hash TEXT NOT NULL
- status TEXT NOT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Vincoli:
- UNIQUE(object_type, object_id, embedding_provider, embedding_model)

## 10.2 `semantic_clusters`
Campi:
- id TEXT PK
- cluster_type TEXT NOT NULL
- label TEXT NULL
- centroid_ref TEXT NULL
- member_count INTEGER DEFAULT 0
- quality_score REAL DEFAULT 0
- metadata_json TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

## 10.3 `semantic_cluster_members`
Campi:
- id TEXT PK
- cluster_id TEXT NOT NULL FK -> semantic_clusters.id
- object_type TEXT NOT NULL
- object_id TEXT NOT NULL
- membership_score REAL DEFAULT 0
- created_at TEXT NOT NULL

---

# 11. Sessioni, feedback e runtime

## 11.1 `sessions`
Campi:
- id TEXT PK
- session_type TEXT NOT NULL
- user_key TEXT NOT NULL
- project_id TEXT NULL FK -> projects.id
- active_context_json TEXT NULL
- active_mode TEXT NOT NULL
- inference_profile TEXT NOT NULL
- autonomy_level TEXT NOT NULL
- started_at TEXT NOT NULL
- ended_at TEXT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

## 11.2 `session_context_items`
Campi:
- id TEXT PK
- session_id TEXT NOT NULL FK -> sessions.id
- object_type TEXT NOT NULL
- object_id TEXT NOT NULL
- context_role TEXT NOT NULL
- rank_score REAL DEFAULT 0
- created_at TEXT NOT NULL

## 11.3 `feedback_events`
Campi:
- id TEXT PK
- user_key TEXT NOT NULL
- target_object_type TEXT NOT NULL
- target_object_id TEXT NOT NULL
- feedback_type TEXT NOT NULL
- score_delta REAL DEFAULT 0
- free_text TEXT NULL
- source_session_id TEXT NULL FK -> sessions.id
- created_at TEXT NOT NULL

Indici:
- idx_feedback_target(target_object_type, target_object_id)
- idx_feedback_user(user_key)

## 11.4 `jobs`
Campi:
- id TEXT PK
- job_type TEXT NOT NULL
- status TEXT NOT NULL
- priority REAL DEFAULT 0
- scheduled_for TEXT NULL
- started_at TEXT NULL
- ended_at TEXT NULL
- retry_count INTEGER DEFAULT 0
- max_retries INTEGER DEFAULT 3
- payload_json TEXT NULL
- result_json TEXT NULL
- error_json TEXT NULL
- actor_type TEXT NOT NULL
- created_at TEXT NOT NULL
- updated_at TEXT NOT NULL

Indici:
- idx_jobs_status(status)
- idx_jobs_type(job_type)
- idx_jobs_schedule(scheduled_for)

## 11.5 `system_state`
Campi:
- id TEXT PK
- state_key TEXT NOT NULL
- state_value_json TEXT NOT NULL
- version INTEGER NOT NULL DEFAULT 1
- updated_at TEXT NOT NULL

Vincoli:
- UNIQUE(state_key)

---

# 12. Audit, controllo e sicurezza

## 12.1 `audit_logs`
Campi:
- id TEXT PK
- event_type TEXT NOT NULL
- actor_type TEXT NOT NULL
- actor_id TEXT NULL
- module_name TEXT NOT NULL
- mode_name TEXT NULL
- action_type TEXT NOT NULL
- target_object_type TEXT NULL
- target_object_id TEXT NULL
- input_refs_json TEXT NULL
- output_refs_json TEXT NULL
- confidence REAL NULL
- reversibility TEXT NOT NULL
- status TEXT NOT NULL
- message TEXT NULL
- metadata_json TEXT NULL
- created_at TEXT NOT NULL

Indici:
- idx_audit_event(event_type)
- idx_audit_target(target_object_type, target_object_id)
- idx_audit_module(module_name)
- idx_audit_created(created_at)

## 12.2 `rollback_points`
Campi:
- id TEXT PK
- scope_type TEXT NOT NULL
- scope_id TEXT NULL
- snapshot_ref TEXT NOT NULL
- created_by TEXT NOT NULL
- reason TEXT NULL
- created_at TEXT NOT NULL

---

# 13. FTS e ricerca

## 13.1 SQLite FTS5
Creare viste/tabella FTS per:
- notes(body_markdown, title, summary)
- chunks(content, title)
- concepts(canonical_label, description)
- decisions(title, description, context_summary)
- procedures(title, description)

Nome suggerito:
- notes_fts
- chunks_fts
- concepts_fts
- decisions_fts
- procedures_fts

---

# 14. Enum suggeriti a livello applicativo

## ingestion_status
- raw_pending
- parsed
- normalized
- failed
- quarantined

## validation_status
- unvalidated
- heuristic
- semantically_validated
- human_validated
- conflicted

## epistemic_type
- fact
- inference
- hypothesis
- suggestion
- verify
- scenario
- conflict
- unknown

## memory_layer
- raw
- processed
- active
- contextual
- strategic
- historical
- latent
- temporary
- episodic
- procedural

## job_status
- queued
- running
- paused
- retrying
- completed
- failed
- cancelled
- awaiting_validation

---

# 15. Vincoli di integrità logica

- nessun `relation` deve puntare a oggetti inesistenti dopo soft delete senza flag `deleted_reference`
- nessun `memory_item` senza oggetto esistente
- nessun `embedding_registry` attivo con hash non coerente all’oggetto corrente
- ogni `decision` importante deve avere almeno una evidenza o rationale
- ogni `scenario` deve avere `premise_json`
- ogni `audit_log` di azione strutturale deve avere target e reversibility
- ogni `goal` ad alta priorità deve avere owner_type e risk_level

---

# 16. Migrazioni e versionamento

- usare Alembic per evoluzione schema
- ogni migrazione deve avere script upgrade/downgrade
- evitare rename distruttivi senza compat layer
- snapshot DB prima di migrazioni di rottura
- aggiornare documento modello dati in parallelo

---

# 17. Definition of Done

Questo schema è completo se:
1. copre tutti gli oggetti cognitivi essenziali
2. supporta memoria multi-livello
3. supporta audit e rollback
4. supporta sessioni, feedback e adattamento
5. supporta job runtime e stato sistema
6. è compatibile con retrieval ibrido
7. è migrabile da SQLite a PostgreSQL
