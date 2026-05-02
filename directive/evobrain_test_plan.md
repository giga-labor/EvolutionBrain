---
doc_id: evobrain-test-plan
title: EvoBrain - Piano di Test
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: quality
extends:
  - evobrain_costituzione_master_index.md
  - evobrain_design_moduli.md
replaces: []
---
# EvoBrain - Piano di Test
## Verifica funzionale, epistemica, cognitiva, operativa e di resilienza

# 1. Scopo

Validare che EvoBrain:
- funzioni tecnicamente
- rispetti i principi epistemici
- non diventi opaco
- non consolidi conoscenza fragile in modo aggressivo
- sia usabile e robusto

---

# 2. Livelli di test

## 2.1 Unit test
Per servizi e utility isolati.

## 2.2 Integration test
Per flussi tra moduli.

## 2.3 API test
Per contratti endpoint.

## 2.4 Epistemic test
Per distinzione fatto/inferenza/ipotesi/scenario.

## 2.5 Cognitive safety test
Per evitare consolidamenti impropri, azioni non autorizzate, drift.

## 2.6 Performance test
Per latenza query, indexing, streaming.

## 2.7 Resilience test
Per fallback, safe mode, recovery.

## 2.8 UX validation test
Per chiarezza di cosa il sistema ha fatto.

---

# 3. Suite minime

## 3.1 Ingestion suite
- import text ok
- import file ok
- duplicate detection ok
- normalization failure quarantined
- reprocess works

## 3.2 Retrieval suite
- keyword search returns exact matches
- semantic search returns conceptually close items
- hybrid search ranking sane
- graph retrieval respects relations
- retrieval trace populated

## 3.3 Knowledge suite
- concept create/update ok
- merge dry-run correct
- merge requires confirmation when impact high
- contradiction relation stored correctly

## 3.4 Memory suite
- score recalculation deterministic within tolerance
- promotion rules applied
- demotion rules applied
- strategic promotion blocked on weak evidence
- memory access updates last_accessed_at

## 3.5 Chat suite
- answer grounded on internal sources
- used_sources returned
- epistemic type present
- no external sources when disabled
- action suggestions separate from answer

## 3.6 Scenario suite
- scenario always labeled scenario
- simulation never promoted to fact automatically
- limitations returned

## 3.7 Audit suite
- mutative actions write audit log
- rollback points created where required
- failed actions still audited

## 3.8 Safety suite
- safe mode blocks restricted operations
- high impact action requires confirmation
- provider failure triggers fallback
- insufficient context lowers confidence or warns

---

# 4. Epistemic acceptance criteria

Per ogni risposta AI verificare:
- presenza tipo epistemico
- presenza fonti interne usate
- nessuna fusione tra inferenza e fatto senza etichetta
- scenario distinto da conoscenza consolidata
- ignoranza dichiarata quando il contesto è insufficiente

---

# 5. Performance target iniziali

- query keyword < 500 ms su dataset medio locale
- query hybrid < 2.5 s in profilo standard
- chat grounded < 5 s con modello remoto normale
- import documento medio < 10 s escluso OCR pesante
- recalcolo memoria progetto medio < 5 s

---

# 6. Resilience tests

- db lock transient recovery
- vector store unavailable fallback
- llm unavailable retrieval-only response
- scheduler crash restart safe
- corrupted job payload quarantined
- rollback restore test

---

# 7. Definition of Done

Il piano di test è soddisfatto se:
1. tutte le suite core passano
2. nessun test epistemico critico fallisce
3. safe mode e fallback verificati
4. performance dentro soglie iniziali ragionevoli
