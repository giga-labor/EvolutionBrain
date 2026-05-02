---
doc_id: evobrain-modello-dati
title: EvoBrain - Modello Dati Completo
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: data-model
extends:
  - evobrain_schema_database.md
  - evobrain_specifica_definitiva_integrata.md
replaces: []
---
# EvoBrain - Modello Dati Completo
## Contratti semantici e strutturali degli oggetti cognitivi

# 1. Scopo

Definire il modello dati logico degli oggetti di EvoBrain, indipendente dal DB ma compatibile con esso.

Ogni oggetto deve avere:
- identità
- stato
- provenienza
- classificazione epistemica
- campi di audit
- relazioni
- metadata estendibile

---

# 2. BaseModel comune

Campi comuni minimi:
- id: str
- object_type: str
- title: str|None
- description: str|None
- status: str
- epistemic_type: str
- confidence: float
- tags: list[str]
- metadata: dict
- related_ids: list[str]
- created_at: datetime
- updated_at: datetime
- version: int

Regole:
- `confidence` tra 0 e 1
- `epistemic_type` obbligatorio per tutti gli oggetti cognitivi
- `metadata` deve essere estendibile ma non sostituire i campi strutturali

---

# 3. DocumentModel

Campi:
- source_type
- source_uri
- source_label
- mime_type
- language
- content_hash
- ingestion_status
- normalization_status
- semantic_status
- validation_status
- project_id
- raw_path
- normalized_path
- quality_score
- size_bytes

---

# 4. ChunkModel

Campi:
- document_id
- chunk_index
- chunk_type
- content
- token_estimate
- char_count
- start_offset
- end_offset
- semantic_status
- lexical_status
- quality_score

---

# 5. NoteModel

Campi:
- note_type
- body_markdown
- summary
- source_type
- project_id
- parent_note_id
- relevance_score
- strategic_weight

Regole:
- `body_markdown` obbligatorio
- se `note_type=decision_note`, deve esistere collegamento a decisione o rationale

---

# 6. ConceptModel

Campi:
- canonical_label
- concept_type
- semantic_centrality_score
- link_density_score
- strategic_weight
- origin
- project_id

Regole:
- `canonical_label` deve essere unico a livello logico per namespace/progetto
- merge solo tramite procedura controllata

---

# 7. EntityModel

Campi:
- name
- entity_type
- canonical_form
- aliases: list[str]
- description

---

# 8. RelationModel

Campi:
- source_object_type
- source_object_id
- target_object_type
- target_object_id
- relation_type
- directionality
- confidence
- validation_status
- origin
- evidence_refs: list[str]

Regole:
- nessuna relazione senza source e target validi
- `origin` in {rule, llm, user, hybrid}
- per `contradicts` confidence minima suggerita >= 0.4

---

# 9. EvidenceModel

Campi:
- evidence_type
- source_object_type
- source_object_id
- strength_score
- quoted_excerpt: str|None
- supporting_refs: list[str]

---

# 10. HypothesisModel

Campi:
- project_id
- support_score
- conflict_score
- open_questions: list[str]
- evidence_refs: list[str]

---

# 11. ScenarioModel

Campi:
- scenario_type
- premise: dict
- assumptions: list[str]
- options: list[dict]
- outputs: dict|None
- limitations: list[str]
- project_id
- risk_score

Regole:
- sempre `epistemic_type=scenario`
- mai promosso a fact automaticamente

---

# 12. ProjectModel

Campi:
- name
- slug
- project_type
- priority
- urgency
- strategic_weight
- owner_type
- active_goal_id
- health_status: str|None
- blockers: list[str]|None

---

# 13. GoalModel

Campi:
- goal_type
- owner_type
- owner_id
- priority
- urgency
- strategic_weight
- due_window_start
- due_window_end
- dependencies: list[str]
- blockers: list[str]
- risk_level

---

# 14. TaskModel

Campi:
- task_type
- project_id
- goal_id
- priority
- urgency
- assignee_type
- assignee_id
- due_at
- started_at
- completed_at
- source_object_ref

---

# 15. DecisionModel

Campi:
- project_id
- goal_id
- decision_type
- context_summary
- rationale: list[str]
- alternatives: list[dict]
- expected_outcomes: list[str]
- review_due_at
- decided_at
- evidence_refs: list[str]
- scenario_refs: list[str]

Regole:
- decisione senza rationale o evidenze va marcata low-confidence

---

# 16. MemoryItemModel

Campi:
- object_type
- object_id
- memory_layer
- memory_score
- recency_score
- frequency_score
- user_interest_score
- project_relevance_score
- strategic_weight
- semantic_centrality_score
- link_density_score
- validation_score
- uncertainty_penalty
- episodic_reinforcement_score
- procedural_utility_score
- decay_factor
- last_accessed_at
- last_scored_at

---

# 17. EpisodeModel

Campi:
- episode_type
- context
- actors
- trigger
- actions
- outcomes
- lessons
- impact_score
- project_id
- started_at
- ended_at

Regole:
- gli episodi servono a memoria esperienziale, non a sostituire concetti
- gli esiti devono poter essere positivi, negativi o misti

---

# 18. ProcedureModel

Campi:
- procedure_type
- steps: list[dict]
- prerequisites: list[str]
- expected_outputs: list[str]
- success_criteria: list[str]
- failure_modes: list[str]
- utility_score
- status
- project_id

Regole:
- ogni step deve avere almeno `order`, `title`, `action`
- procedure può collegarsi a episodi di successo/fallimento

---

# 19. UserModel

Campi:
- user_key
- preferences
- style_profile
- dominant_projects
- response_preferences
- query_patterns
- decision_patterns
- constraints
- adaptation_profile

---

# 20. SelfModel

Campi:
- self_name
- self_role
- mission_profile
- active_capabilities
- disabled_capabilities
- risk_tolerance_profile
- autonomy_level
- trust_profile
- known_limits
- current_operational_state
- current_focus
- current_load
- current_confidence
- recent_failures
- recent_successes
- adaptation_state

Regole:
- mutazioni ad alto impatto richiedono validazione forte
- non usare come memoria generica

---

# 21. SessionModel

Campi:
- session_type
- user_key
- project_id
- active_context
- active_mode
- inference_profile
- autonomy_level
- started_at
- ended_at

---

# 22. FeedbackEventModel

Campi:
- user_key
- target_object_type
- target_object_id
- feedback_type
- score_delta
- free_text
- source_session_id

---

# 23. JobModel

Campi:
- job_type
- status
- priority
- scheduled_for
- started_at
- ended_at
- retry_count
- max_retries
- payload
- result
- error
- actor_type

---

# 24. AuditLogModel

Campi:
- event_type
- actor_type
- actor_id
- module_name
- mode_name
- action_type
- target_object_type
- target_object_id
- input_refs
- output_refs
- confidence
- reversibility
- status
- message
- metadata

---

# 25. Pydantic contracts suggeriti

Classi minime:
- DocumentIn / DocumentOut
- NoteCreate / NoteUpdate / NoteOut
- ConceptCreate / ConceptMergePlan / ConceptOut
- SearchRequest / SearchResult / SearchResponse
- ChatQueryRequest / ChatResponse
- ProjectCreate / ProjectOut
- GoalCreate / GoalOut
- TaskCreate / TaskOut
- DecisionCreate / DecisionOut
- MemoryItemOut / MemoryDashboardOut
- ScenarioCreate / ScenarioSimulationOut
- AuditLogOut
- JobCreate / JobOut
- SelfModelOut / UserModelOut

---

# 26. Regole di serializzazione

- usare camelCase in frontend se necessario, ma snake_case come canonico backend
- date ISO8601
- enum esplicitati in docs
- payload con campi ignoti accettati solo in metadata

---

# 27. Definition of Done

Il modello dati è completo se:
1. ogni oggetto ha identità, stato, epistemologia e auditability
2. gli oggetti coprono memoria, conoscenza, progetti, runtime e controllo
3. i contratti sono sufficienti per backend e frontend
4. esiste separazione chiara tra scenario, ipotesi, fatto e decisione
