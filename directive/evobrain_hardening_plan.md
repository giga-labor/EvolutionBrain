---
doc_id: evobrain-hardening-plan
title: EvoBrain - Piano di Hardening
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L4
domain: security
extends:
  - evobrain_costituzione_master_index.md
  - evobrain_modalita_operative_reali.md
replaces: []
---
# EvoBrain - Piano di Hardening
## Robustezza, resilienza, sicurezza cognitiva e recovery

# 1. Scopo

Rendere EvoBrain sicuro, resistente e recuperabile sotto:
- errori runtime
- crash processo
- fallimenti provider
- drift adattivo
- operazioni cognitive ad alto impatto
- corruzione parziale dati

---

# 2. Misure obbligatorie

## 2.1 Backup
- backup incrementali giornalieri
- snapshot prima di migrazioni critiche
- export manuale on-demand

## 2.2 Rollback
- rollback points per merge, pruning, restore strategici
- restore testato

## 2.3 Safe mode
- attivabile manualmente e automaticamente
- blocca mutazioni ad alto impatto
- consente retrieval base e consultazione

## 2.4 Quarantine
- file/documenti/job problematici spostati in stato quarantined
- nessun reprocessing infinito

## 2.5 Idempotenza
- import documenti e jobs ripetibili senza duplicati strutturali

---

# 3. Hardening cognitivo

- blocco promozione strategica su evidenza debole
- merge concetti con dry-run obbligatorio
- separazione scenario/fatto sempre enforced
- review periodica drift
- contradiction scan settimanale
- audit di ogni mutazione cognitiva

---

# 4. Hardening tecnico

- timeout su chiamate provider
- retry limitato con backoff
- lock job con lease
- journaling eventi critici
- health checks moduli
- circuit breaker su provider instabili

---

# 5. Observability minima

- logs strutturati JSON
- metriche latency/error rate
- queue depth
- jobs stuck
- safe mode events
- provider outage count
- rollback count

---

# 6. Definition of Done

Hardening completo se:
1. esiste recovery da crash e provider outage
2. safe mode reale verificato
3. backup/rollback operativi
4. mutazioni cognitive ad alto impatto protette
