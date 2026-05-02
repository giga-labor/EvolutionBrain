---
doc_id: evobrain-design-moduli
title: EvoBrain - Design Tecnico dei Moduli
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: architecture
extends:
  - evobrain_specifica_definitiva_integrata.md
  - evobrain_schema_api.md
  - evobrain_schema_database.md
replaces: []
---
# EvoBrain - Design Tecnico dei Moduli
## Architettura interna, contratti tra componenti e orchestrazione concreta

# 1. Scopo

Tradurre l’architettura concettuale di EvoBrain in moduli tecnici implementabili, separati e testabili.

---

# 2. Mappa dei moduli

Struttura suggerita:
```text
app/
  api/
  core/
  ingestion/
  normalization/
  semantic/
  retrieval/
  knowledge/
  memory/
  attention/
  goals/
  reasoning/
  simulation/
  metacognition/
  adaptation/
  actions/
  audit/
  scheduler/
  ui_backend/
```

---

# 3. Modulo `core`

Responsabilità:
- configurazione globale
- dependency injection
- feature flags
- enums comuni
- error handling
- utilità shared
- request context

Contratti:
- ConfigService
- FeatureFlagService
- ClockService
- IdService
- EventBus

---

# 4. Modulo `ingestion`

Responsabilità:
- import contenuti
- hashing
- dedupe preliminare
- creazione document record
- enqueue pipeline

Interfacce:
- IngestionService.import_text()
- IngestionService.import_file()
- IngestionService.import_uri()
- IngestionService.reprocess_document()

Input:
- source payload
Output:
- document_id
- job_id
- ingestion result

---

# 5. Modulo `normalization`

Responsabilità:
- parsing per tipo file
- cleanup
- chunking
- metadata extraction
- classification

Interfacce:
- NormalizationService.normalize_document(document_id)
- ChunkingService.chunk_text()
- ClassificationService.classify_content()

Output:
- normalized document
- chunks
- metadata

---

# 6. Modulo `semantic`

Responsabilità:
- embeddings
- lexical indexing
- entity extraction
- concept candidate extraction
- relation proposals
- clustering

Interfacce:
- EmbeddingService.embed_object()
- LexicalIndexService.index_note()
- EntityExtractionService.extract()
- RelationProposalService.propose()
- ClusterService.refresh()

Dipendenze:
- llm abstraction
- vector store adapter
- fts adapter

---

# 7. Modulo `retrieval`

Responsabilità:
- query planning
- retrieval lessicale
- retrieval semantico
- retrieval da grafo
- ranking finale
- context assembly

Sottocomponenti:
- QueryPlanner
- LexicalRetriever
- SemanticRetriever
- GraphRetriever
- ResultRanker
- ContextAssembler

Interfacce:
- RetrievalService.search(request)
- RetrievalService.build_context(query, filters, session)

Output:
- ranked results
- retrieval trace
- context bundle

---

# 8. Modulo `knowledge`

Responsabilità:
- creare/aggiornare concetti
- gestire merge
- consolidare relazioni
- aggiornare evidence/hypotheses/scenarios
- integrity rules per knowledge base

Interfacce:
- KnowledgeService.upsert_concept()
- KnowledgeService.merge_concepts()
- KnowledgeService.create_relation()
- KnowledgeService.consolidate_project_scope()

Richiede:
- audit
- validation policies
- confirmation flow per merge critici

---

# 9. Modulo `memory`

Responsabilità:
- memory layers
- scoring
- promotion/demotion
- access tracking
- decay
- daily/weekly memory maintenance

Sottocomponenti:
- MemoryScoringEngine
- MemoryLayerManager
- PromotionPolicy
- DemotionPolicy
- AccessTracker

Interfacce:
- MemoryService.recalculate(scope)
- MemoryService.promote(...)
- MemoryService.demote(...)
- MemoryService.record_access(...)

---

# 10. Modulo `attention`

Responsabilità:
- selezionare focus cognitivo
- decidere top-K oggetti di lavoro
- ridurre rumore
- gestire saturazione

Interfacce:
- AttentionService.compute_focus(session_id)
- AttentionService.rank_salience(items, context)

Input:
- session
- project
- urgency
- goals
- memory scores
- recent actions

Output:
- focus primary
- focus secondary
- dropped items
- salience trace

---

# 11. Modulo `goals`

Responsabilità:
- gestire goal e priorità
- conflitti tra goal
- priorità breve/medio/lungo termine
- task derivation
- blocker analysis

Interfacce:
- GoalService.recalculate_priorities()
- GoalService.resolve_conflicts()
- GoalService.derive_tasks(goal_id)

Output:
- ordered goal list
- blocker map
- suggested next actions

---

# 12. Modulo `reasoning`

Responsabilità:
- intent classification
- mode selection
- response planning
- llm orchestration
- epistemic labeling
- answer construction

Sottocomponenti:
- IntentClassifier
- ModeSelector
- ResponsePlanner
- LLMRouter
- EpistemicLabeler
- AnswerBuilder

Interfacce:
- ReasoningService.answer_chat(request)
- ReasoningService.compare_objects(...)
- ReasoningService.summarize_scope(...)

Regola:
- usare prima retrieval/context, poi LLM

---

# 13. Modulo `simulation`

Responsabilità:
- gestire scenari
- costruire alternative
- sandbox reasoning
- separazione scenario/fatto
- outcome formatting

Interfacce:
- SimulationService.create_scenario(...)
- SimulationService.run_scenario(...)
- SimulationService.compare_scenarios(...)

---

# 14. Modulo `metacognition`

Responsabilità:
- quality self-check
- context sufficiency estimation
- overconfidence risk
- drift signal detection
- fallback recommendation

Interfacce:
- MetacognitionService.evaluate_response_plan(...)
- MetacognitionService.evaluate_output(...)
- MetacognitionService.system_snapshot()

Output:
- quality flags
- warnings
- downgrade/escalation suggestions

---

# 15. Modulo `adaptation`

Responsabilità:
- ingest feedback
- ranking updates
- profile updates
- safe adaptive tuning
- drift guardrails

Interfacce:
- AdaptationService.apply_feedback(...)
- AdaptationService.recalibrate(...)
- AdaptationService.detect_drift()

Regola:
- ogni update adattivo deve essere auditabile

---

# 16. Modulo `actions`

Responsabilità:
- esecuzione concreta di mutazioni
- create/update/archive/link/merge
- dry-run
- confirmation flows
- rollback point creation

Interfacce:
- ActionService.execute(action_request)
- ActionService.plan(action_request)
- ActionService.requires_confirmation(action_request)

---

# 17. Modulo `audit`

Responsabilità:
- log strutturati
- rollback points
- trace di reasoning e retrieval
- report integrità

Interfacce:
- AuditService.log_event(...)
- AuditService.create_rollback_point(...)
- AuditService.query_logs(...)

---

# 18. Modulo `scheduler`

Responsabilità:
- orchestration batch jobs
- periodic maintenance
- daily/weekly review
- retries
- dead job recovery

Interfacce:
- SchedulerService.enqueue(...)
- SchedulerService.run_due_jobs()
- SchedulerService.retry(job_id)

---

# 19. Modulo `api`

Responsabilità:
- esposizione endpoint
- validazione request/response
- auth/logical permission
- streaming adapters

Controller groups:
- system
- chat
- search
- documents
- notes
- concepts
- projects
- tasks
- decisions
- memory
- scenarios
- feedback
- audit
- jobs

---

# 20. Adapters esterni

## 20.1 LLMAdapter
Metodi:
- classify()
- summarize()
- extract()
- reason()
- simulate()

## 20.2 VectorStoreAdapter
Metodi:
- upsert()
- query()
- delete()
- health()

## 20.3 LexicalIndexAdapter
Metodi:
- index()
- search()
- rebuild()

## 20.4 StorageAdapter
Metodi:
- save_raw()
- save_normalized()
- read()
- exists()

---

# 21. Orchestratore principale

`BrainOrchestrator` coordina i moduli.

Flusso chat:
1. intent classification
2. mode selection
3. query planning
4. retrieval
5. attention focus refinement
6. metacognition pre-check
7. llm routing / reasoning
8. epistemic labeling
9. action planning
10. audit

Flusso ingestion:
1. import
2. document record
3. normalization
4. semantic indexing
5. knowledge updates
6. memory updates
7. audit

---

# 22. Event bus interno

Eventi minimi:
- document_imported
- document_normalized
- semantic_indexed
- concept_created
- relation_proposed
- memory_promoted
- memory_demoted
- goal_updated
- decision_created
- job_failed
- safe_mode_changed
- feedback_received

Event bus iniziale:
- sincrono semplice o pub/sub locale
- evolvibile verso coda dedicata

---

# 23. Sequence concrete

## 23.1 Query utente
API -> Reasoning -> Retrieval -> Attention -> Metacognition(pre) -> LLMRouter -> Metacognition(post) -> ActionPlanner(optional) -> Audit -> API response

## 23.2 Import documento
API -> Ingestion -> Normalization -> Semantic -> Knowledge -> Memory -> Audit

## 23.3 Consolidamento notturno
Scheduler -> Knowledge.consolidate -> Memory.recalculate -> Adaptation.drift_check -> Audit

---

# 24. Regole di dipendenza

- `api` non deve contenere logica cognitiva
- `reasoning` non deve scrivere direttamente nel DB: passa da `actions` o service dedicati
- `adaptation` non modifica strutture strategiche senza `actions` + audit
- `metacognition` non decide, raccomanda
- `attention` non muta memoria, seleziona focus
- `knowledge` e `memory` devono restare separati

---

# 25. Definition of Done

Il design moduli è completo se:
1. ogni dominio ha responsabilità chiare
2. i contratti tra moduli sono definiti
3. esiste un orchestratore chiaro
4. i moduli centrali sono testabili in isolamento
5. i side effects passano da azioni e audit
