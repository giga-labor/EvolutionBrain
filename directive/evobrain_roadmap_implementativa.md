---
doc_id: evobrain-roadmap-implementativa
title: EvoBrain - Roadmap Implementativa
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: planning
extends:
  - evobrain_specifica_definitiva_integrata.md
  - evobrain_design_moduli.md
replaces: []
---
# EvoBrain - Roadmap Implementativa
## Ordine reale di sviluppo e milestone tecniche

# 1. Fase 0 — Fondazione tecnica
- repo setup
- config base
- sqlite + alembic
- file storage
- audit minimal
- health endpoints

Deliverable:
- skeleton funzionante

# 2. Fase 1 — Ingestion e note
- import text/file
- documents/chunks/notes
- normalization
- search keyword base
- UI minimale per note + chat base

Deliverable:
- vault interrogabile

# 3. Fase 2 — Retrieval ibrido
- vector store
- embeddings
- hybrid search
- context assembly
- chat grounded

Deliverable:
- chat realmente basata su fonti interne

# 4. Fase 3 — Knowledge & Projects
- concepts/entities/relations
- projects/goals/tasks/decisions
- workspace progetto
- explorer relazionale base

Deliverable:
- sistema utilizzabile per lavori veri

# 5. Fase 4 — Memory engine
- memory_items
- scoring
- promotion/demotion
- memory dashboard
- daily/weekly review

Deliverable:
- memoria evolutiva operativa

# 6. Fase 5 — Funzioni cognitive profonde
- attention engine
- episodic memory
- procedural memory
- scenario engine
- self model
- user model

Deliverable:
- cervello molto più completo

# 7. Fase 6 — Metacognition e adaptation
- metacognitive monitor
- feedback loops
- adaptation recalibration
- drift detection
- contradiction scan

Deliverable:
- sistema più maturo e controllato

# 8. Fase 7 — Hardening
- safe mode
- rollback
- backup
- scheduler robusto
- observability

Deliverable:
- piattaforma stabile

# 9. Fase 8 — Refinement UI
- dashboards finali
- graph view migliore
- simulation view
- audit console completa
