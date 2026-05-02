---
doc_id: evobrain-secondo-cervello-spec
title: EvoBrain - Specifica completa per AI Builder
version: 0.9.0
updated_at: 2026-04-27
status: deprecated
authority_level: historical
domain: architecture
extends: []
replaces: []
deprecated_by:
  - evobrain_specifica_definitiva_integrata.md
---

> Stato documento: `deprecated` (storico).  
> Usare come fonte autorevole `evobrain_specifica_definitiva_integrata.md`.

# Specifica completa per AI Builder
## Sistema di Secondo Cervello Evolutivo Superintelligente, Intuitivo, Dinamico, Adattabile e Rapido

## 1. Scopo generale

Costruisci un sistema software completo chiamato **EvoBrain** progettato come **secondo cervello evolutivo**.  
Il sistema deve funzionare come una struttura cognitiva esterna capace di:

- acquisire informazioni da fonti diverse
- organizzarle in modo leggibile e strutturato
- comprenderne il significato
- trasformarle in conoscenza utile
- mantenere memoria storica e memoria attiva
- adattarsi nel tempo in base all’uso reale
- assistere il proprietario nei processi di pensiero, decisione, scrittura, pianificazione, apprendimento e sviluppo di progetti
- aggiornare dinamicamente priorità, collegamenti e concetti rilevanti
- essere veloce, modulare, estendibile e controllabile

Il sistema **non deve essere un semplice chatbot che legge file**, ma una vera architettura cognitiva esterna composta da più livelli cooperanti.

---

## 2. Obiettivo architetturale

L’AI deve generare un sistema che abbia queste proprietà fondamentali:

1. **Persistenza reale della conoscenza**  
   Tutto ciò che conta deve poter essere salvato, recuperato, versionato e aggiornato.

2. **Comprensione semantica**  
   Il sistema deve lavorare non solo sul testo, ma sul significato.

3. **Memoria gerarchica e dinamica**  
   Non tutto deve avere lo stesso peso. Serve distinzione tra attivo, storico, strategico, latente, temporaneo.

4. **Evoluzione continua**  
   Il sistema deve imparare dal contenuto e anche dal comportamento dell’utente.

5. **Modularità totale**  
   Ogni componente deve essere sostituibile senza distruggere il sistema.

6. **Interoperabilità**  
   Il cuore del sistema deve restare indipendente dal singolo provider LLM.

7. **Verificabilità**  
   Le inferenze devono essere tracciabili. Distinguere sempre fatto, deduzione, ipotesi e suggerimento.

8. **Rapidità operativa**  
   Minimizzare chiamate inutili al modello. Usare prima dati, indici, regole, memoria e solo dopo l’LLM.

9. **Intuitività**  
   L’interazione deve essere semplice: chat, comandi, pannello, query naturali, scorciatoie operative.

10. **Adattabilità**  
    Il sistema deve poter funzionare in locale, ibrido o cloud, con modelli locali o remoti.

---

## 3. Filosofia di progettazione

L’AI che implementa il sistema deve rispettare queste regole:

- Il sistema deve essere **human-readable first**
- Il contenuto base deve restare accessibile senza AI
- Il formato dei dati deve essere il più possibile aperto
- Il sistema deve separare chiaramente:
  - memoria grezza
  - memoria elaborata
  - memoria attiva
  - memoria strategica
  - memoria storica
- L’LLM non deve essere il centro dell’architettura: deve essere un modulo di elaborazione
- Il sistema deve saper funzionare in modo degradato anche senza LLM
- Ogni automazione critica deve essere loggata
- Ogni trasformazione importante deve essere reversibile
- Il rumore va controllato in automatico
- La crescita del sistema non deve portare caos, ma consolidamento progressivo

---

## 4. Requisiti funzionali principali

Il sistema deve saper fare almeno queste cose:

### 4.1 Acquisizione
- importare file Markdown
- importare testo semplice
- importare PDF e documenti convertendoli in contenuto indicizzabile
- importare trascrizioni audio
- importare conversazioni
- importare pagine web o link salvati
- importare note rapide manuali
- importare file da cartelle monitorate

### 4.2 Normalizzazione
- pulire il contenuto
- uniformare encoding, metadati e naming
- deduplicare note simili o identiche
- segmentare documenti lunghi in blocchi coerenti
- estrarre entità, concetti, persone, date, progetti, decisioni, task, domande aperte
- classificare il contenuto per tipologia

### 4.3 Indicizzazione
- creare indice full-text
- creare indice semantico vettoriale
- creare grafo relazionale tra concetti, note, progetti e persone
- mantenere versioni degli indici sincronizzate con i documenti

### 4.4 Memoria
- distinguere memoria grezza, attiva, strategica, storica, latente e temporanea
- assegnare punteggi dinamici di rilevanza
- aggiornare la priorità dei contenuti in base all’uso, al tempo e al contesto
- conservare relazioni tra vecchi e nuovi concetti
- fare consolidamento periodico della memoria

### 4.5 Ragionamento
- rispondere a domande usando memoria e fonti reali
- confrontare note o idee
- generare sintesi
- rilevare contraddizioni
- estrarre concetti stabili
- produrre schede di conoscenza
- collegare informazioni sparse
- identificare temi emergenti
- trasformare materiale grezzo in conoscenza strutturata
- distinguere sempre fatti da ipotesi

### 4.6 Operatività
- creare note automaticamente
- aggiornare schede progetto
- generare riepiloghi periodici
- proporre piani di azione
- creare checklist
- trasformare idee in task
- collegare decisioni a motivazioni e fonti
- costruire timeline di progetto o concettuali

### 4.7 Evoluzione
- apprendere dalle correzioni dell’utente
- apprendere dai pattern d’uso
- aggiornare priorità e pesi
- riconoscere aree ricorrenti
- modificare il comportamento dei moduli in base all’efficacia
- tracciare ciò che è stato utile e ciò che non lo è stato

---

## 5. Requisiti non funzionali

Il sistema deve essere:

- modulare
- estendibile
- robusto
- ispezionabile
- veloce
- recuperabile in caso di errore
- trasparente nei processi
- efficiente nei costi inferenziali
- adatto a grandi volumi di note
- utilizzabile anche offline in modalità parziale
- pensato per lunga durata, non per demo effimere

---

## 6. Architettura ideale a strati

L’AI deve implementare la seguente architettura.

## 6.1 Strato 1 — Ingestion Layer
Responsabilità:
- acquisizione da tutte le fonti
- hashing dei contenuti
- metadata extraction iniziale
- version tracking
- queue di processamento

Output:
- documenti raw registrati
- job di normalizzazione in coda

## 6.2 Strato 2 — Normalization Layer
Responsabilità:
- parsing
- cleanup
- deduplica
- chunking intelligente
- classificazione tipologica
- estrazione metadati strutturati

Output:
- unità informative normalizzate
- riferimenti alla fonte originale
- flag di qualità del contenuto

## 6.3 Strato 3 — Semantic Layer
Responsabilità:
- embedding generation
- indicizzazione vettoriale
- entity linking
- concept extraction
- relation discovery
- similarity clustering

Output:
- indice semantico
- concetti candidati
- relazioni candidate
- cluster tematici

## 6.4 Strato 4 — Knowledge Layer
Responsabilità:
- trasformare i contenuti in oggetti cognitivi
- mantenere knowledge objects persistenti
- aggiornare concetti, persone, progetti, decisioni, regole, preferenze, domande aperte

Output:
- knowledge base strutturata

## 6.5 Strato 5 — Memory Layer
Responsabilità:
- gestione della memoria multi-livello
- promozione e declassamento delle informazioni
- scoring di attivazione
- decay controllato
- consolidamento periodico

Output:
- memoria attiva
- memoria strategica
- memoria storica
- memoria latente

## 6.6 Strato 6 — Reasoning Layer
Responsabilità:
- orchestrare query, retrieval, sintesi e inferenza
- combinare ricerca lessicale, semantica e grafo
- costruire contesto mirato per i modelli
- generare risposte, confronti e sintesi

Output:
- risposte motivate
- inferenze classificate
- proposte operative
- aggiornamenti di conoscenza

## 6.7 Strato 7 — Identity and Adaptation Layer
Responsabilità:
- rappresentare obiettivi, valori operativi, preferenze, priorità e vincoli
- apprendere dagli usi reali
- adattare scoring, retrieval, ranking e comportamenti

Output:
- profilo cognitivo operativo
- parametri di adattamento
- storico evolutivo

## 6.8 Strato 8 — Action Layer
Responsabilità:
- creare/aggiornare note
- scrivere schede progetto
- aggiornare dashboard
- lanciare job pianificati
- generare output pronti all’uso

Output:
- artefatti
- aggiornamenti automatici
- report

## 6.9 Strato 9 — Audit and Control Layer
Responsabilità:
- logging completo
- explainability
- rollback
- distinzione fatto/ipotesi
- verifica qualità
- monitoraggio performance

Output:
- audit trail completo
- controlli di coerenza
- error reports

---

## 7. Tipi di memoria da implementare

Il sistema deve implementare memoria con stati distinti.

### 7.1 Memoria grezza
Contiene materiale acquisito non ancora consolidato.  
Serve come archivio sorgente.

### 7.2 Memoria elaborata
Contiene contenuti puliti, segmentati, arricchiti e indicizzati.

### 7.3 Memoria attiva
Contiene ciò che è rilevante ora per l’utente, per il contesto e per i progetti in corso.

### 7.4 Memoria contestuale
Contiene materiale utile nel tema o conversazione corrente.

### 7.5 Memoria strategica
Contiene obiettivi stabili, vincoli, preferenze persistenti, direzioni di lavoro, concetti chiave.

### 7.6 Memoria storica
Contiene tutto ciò che resta importante come archivio di lungo periodo.

### 7.7 Memoria latente
Contiene contenuti non prioritari ma potenzialmente utili in futuro.

### 7.8 Memoria temporanea
Contiene lo stato volatile di task, sessioni e ragionamenti in corso.

---

## 8. Oggetti cognitivi da modellare

Il sistema non deve limitarsi a salvare file.  
Deve costruire e mantenere oggetti cognitivi strutturati.

Tipi minimi:

- Note
- Documenti
- Chunk
- Concetti
- Entità
- Persone
- Luoghi
- Progetti
- Sottoprogetti
- Obiettivi
- Vincoli
- Decisioni
- Evidenze
- Ipotesi
- Domande aperte
- Task
- Routine
- Regole operative
- Preferenze
- Pattern ricorrenti
- Timeline event
- Relazioni tra oggetti

Ogni oggetto deve avere almeno:
- id stabile
- tipo
- titolo o label
- descrizione
- fonte/i
- timestamp creazione
- timestamp aggiornamento
- confidenza
- stato
- tag
- collegamenti
- punteggio rilevanza
- versione

---

## 9. Struttura dati consigliata

Usa una combinazione ibrida:

### 9.1 File system
Per contenuti human-readable:
- `vault/raw/`
- `vault/normalized/`
- `vault/notes/`
- `vault/projects/`
- `vault/daily/`
- `vault/concepts/`
- `vault/reports/`
- `vault/archive/`

### 9.2 Database relazionale
Usa SQLite per la prima versione, con possibilità di migrazione a PostgreSQL.

Tabelle suggerite:
- documents
- chunks
- concepts
- entities
- projects
- tasks
- decisions
- evidence
- hypotheses
- preferences
- memory_items
- relations
- embeddings_registry
- sessions
- feedback_events
- audit_logs
- jobs
- system_state

### 9.3 Vector store
Supportare almeno una di queste opzioni:
- FAISS
- Chroma
- Qdrant
- LanceDB

### 9.4 Grafo relazionale
Implementare almeno:
- relazione concetto-concetto
- concetto-documento
- progetto-decisione
- progetto-task
- persona-progetto
- evidenza-ipotesi
- nota-nota
- concetto-domanda aperta

---

## 10. Organizzazione cartelle suggerita

```text
evobrain/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ ingestion/
│  ├─ normalization/
│  ├─ semantic/
│  ├─ memory/
│  ├─ reasoning/
│  ├─ adaptation/
│  ├─ actions/
│  ├─ audit/
│  ├─ scheduler/
│  └─ ui/
├─ config/
├─ data/
│  ├─ vault/
│  ├─ db/
│  ├─ vector/
│  ├─ graph/
│  ├─ logs/
│  └─ cache/
├─ tests/
├─ scripts/
├─ docs/
├─ prompts/
├─ models/
└─ README.it.md
```

---

## 11. Stack tecnologico consigliato

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- APScheduler o equivalente

### Database
- SQLite iniziale
- PostgreSQL opzionale per crescita

### Vector Search
- FAISS o Chroma iniziale
- Qdrant opzionale per scala maggiore

### Search lessicale
- SQLite FTS5 oppure Whoosh/BM25
- opzionalmente Elasticsearch/OpenSearch in fasi avanzate

### Grafo
- networkx iniziale
- Neo4j opzionale in fase avanzata

### Frontend
- web UI semplice e rapida
- pannello con:
  - chat
  - ricerca
  - knowledge explorer
  - memory dashboard
  - project view
  - audit view

### LLM abstraction
Implementare un layer astratto che supporti:
- modelli locali
- modelli remoti via API
- fallback tra provider
- routing per task diversi

Modelli intercambiabili:
- summarizer model
- extractor model
- reasoning model
- classifier model
- fast local helper model

---

## 12. Regola fondamentale sul ruolo dell’LLM

L’AI che costruisce il sistema deve seguire questo principio:

**Usare il modello solo quando serve comprensione o generazione.**  
Non usare il modello per compiti che possono essere fatti meglio da:
- database
- ricerca testuale
- punteggi
- regole
- hashing
- grafi
- pipeline deterministiche

Ordine decisionale corretto:
1. cerca nella memoria strutturata
2. cerca negli indici
3. cerca nel grafo
4. usa regole e scoring
5. solo dopo costruisci contesto e chiama LLM

---

## 13. Motore di orchestrazione

Implementa un orchestratore centrale che decida:
- quale modulo usare
- quale memoria consultare
- quali fonti recuperare
- quanta finestra di contesto costruire
- quale modello invocare
- se il compito richiede:
  - retrieval
  - sintesi
  - estrazione
  - confronto
  - scrittura
  - aggiornamento memoria
  - verifica coerenza

L’orchestratore deve gestire:
- task routing
- budget inferenziale
- timeout
- fallback
- scoring qualità
- caching risultati

---

## 14. Pipeline di ingestione e consolidamento

### 14.1 Pipeline ingestione
1. rileva nuova fonte
2. importa contenuto
3. calcola hash
4. verifica duplicati
5. salva raw
6. normalizza
7. chunking
8. embedding
9. indexing
10. entity extraction
11. concept candidate extraction
12. relation candidate extraction
13. audit log
14. aggiornamento knowledge layer

### 14.2 Pipeline consolidamento periodico
1. analizza contenuti recenti
2. identifica concetti ricorrenti
3. fonde duplicati concettuali
4. promuove elementi da latenti a strategici se necessario
5. declassa ciò che perde rilevanza
6. aggiorna relazioni
7. produce report evolutivo
8. salva snapshot della memoria

---

## 15. Sistema di scoring della memoria

Ogni elemento deve avere un punteggio composito.  
Esempio di componenti:

- recency_score
- frequency_score
- user_interest_score
- project_relevance_score
- strategic_weight
- semantic_centrality_score
- link_density_score
- validation_score
- uncertainty_penalty
- decay_factor

Formula generale suggerita:

```text
memory_score =
  (w1 * recency_score) +
  (w2 * frequency_score) +
  (w3 * user_interest_score) +
  (w4 * project_relevance_score) +
  (w5 * strategic_weight) +
  (w6 * semantic_centrality_score) +
  (w7 * link_density_score) +
  (w8 * validation_score) -
  (w9 * uncertainty_penalty)
all multiplied by decay_factor
```

Il sistema deve permettere:
- pesi configurabili
- aggiornamento dei pesi nel tempo
- apprendimento parziale dai feedback
- override manuali

---

## 16. Adattamento evolutivo

Il sistema deve evolvere nel tempo usando almeno queste fonti:

- feedback esplicito dell’utente
- correzioni dell’utente
- consultazioni frequenti
- query ricorrenti
- note spesso richiamate
- schede progetto più usate
- task realmente completati
- suggerimenti accettati o rifiutati

Adattamenti possibili:
- ranking dei risultati
- promozione di concetti
- modifica delle soglie
- variazione del peso dei progetti
- modifica del comportamento del retriever
- personalizzazione dei riepiloghi
- personalizzazione del tono operativo

Il sistema deve avere memoria dell’evoluzione, non solo dello stato attuale.

---

## 17. Distinzione epistemica obbligatoria

Ogni output intelligente deve classificare i contenuti almeno come:

- **Fatto**
- **Inferenza**
- **Ipotesi**
- **Suggerimento**
- **Contenuto da verificare**

Questa distinzione deve valere sia nelle risposte sia nella base di conoscenza.

Mai mischiare liberamente dati reali e deduzioni senza etichettatura.

---

## 18. Controllo allucinazioni e qualità

Implementare sistemi di protezione:

- citazione delle fonti interne
- link alla nota originale
- score di confidenza
- controllo contraddizioni note
- refusal controllato su bassa evidenza
- revisione automatica delle inferenze deboli
- doppio passaggio per aggiornamenti critici
- audit trail dettagliato

Per modifiche strutturali alla knowledge base:
- proporre
- validare
- poi consolidare

---

## 19. Interfacce richieste

Il sistema deve avere almeno:

### 19.1 Chat operativa
Capacità:
- domande in linguaggio naturale
- ragionamento su contenuti
- query multi-documento
- riassunti
- confronto tra idee
- azioni su note/progetti

### 19.2 Ricerca avanzata
Supporto:
- keyword
- full text
- semantica
- filtri per tipo, data, progetto, stato, confidenza

### 19.3 Dashboard memoria
Mostrare:
- contenuti più attivi
- temi emergenti
- progetti caldi
- concetti in crescita
- aree trascurate
- relazioni recenti
- elementi da validare

### 19.4 Vista grafo
Permettere esplorazione relazionale di:
- note
- concetti
- progetti
- decisioni
- persone
- evidenze

### 19.5 Vista progetto
Ogni progetto deve mostrare:
- scopo
- stato
- note collegate
- decisioni
- task
- problemi aperti
- cronologia

### 19.6 Audit panel
Mostrare:
- trasformazioni
- inferenze generate
- modifiche automatiche
- errori
- revisioni richieste
- rollback disponibili

---

## 20. Modalità operative del sistema

Il sistema deve supportare almeno queste modalità:

### 20.1 Passive capture mode
Assorbe contenuti e li struttura senza disturbare.

### 20.2 Active assistant mode
Risponde, sintetizza, collega, suggerisce.

### 20.3 Research mode
Analizza argomenti, costruisce mappe concettuali, confronta fonti.

### 20.4 Project co-pilot mode
Segue i progetti nel tempo, aggiorna stato e priorità.

### 20.5 Reflection mode
Esegue consolidamento, identifica pattern, produce sintesi metacognitive.

### 20.6 Maintenance mode
Deduplica, ripulisce, ricostruisce indici, verifica integrità.

---

## 21. Regole per le note Markdown

Le note devono restare leggibili e usabili anche senza AI.

Formato consigliato:

```md
---
id: unique-id
type: note|concept|project|decision|task|evidence|hypothesis
title: Titolo
created_at: 2026-04-23T10:00:00
updated_at: 2026-04-23T10:00:00
source: manual|import|chat|web|pdf|audio
status: active
tags: [tag1, tag2]
confidence: 0.85
project: nome-progetto
related: [id1, id2]
---

# Titolo

## Sintesi
...

## Contenuto
...

## Concetti estratti
- ...

## Decisioni
- ...

## Domande aperte
- ...

## Collegamenti
- [[altra-nota]]
```

---

## 22. Regole per il knowledge extraction

Ogni volta che arriva nuovo contenuto, il sistema deve tentare di estrarre:

- tema principale
- sotto-temi
- concetti chiave
- entità nominate
- relazioni implicite
- decisioni esplicite
- desideri o obiettivi
- problemi
- vincoli
- task potenziali
- domande aperte
- materiale contraddittorio con conoscenza esistente

L’estrazione deve essere conservativa: meglio meno ma accurato, non molto ma sbagliato.

---

## 23. Modello relazionale minimo

Ogni relazione deve avere:
- id
- source_id
- target_id
- relation_type
- confidence
- evidence_refs
- created_at
- updated_at
- origin (rule|llm|user|hybrid)

Tipi minimi:
- related_to
- supports
- contradicts
- derives_from
- belongs_to
- depends_on
- decided_by
- about
- extends
- similar_to
- unresolved_with

---

## 24. Scheduler e automazioni

Implementare job schedulati per:

- rebuild indici
- consolidamento memoria
- deduplica
- sintesi giornaliera
- sintesi settimanale
- aggiornamento dashboard
- verifica integrità database
- report anomalie
- export backup

---

## 25. Backup, snapshot e recupero

Il sistema deve avere:
- backup incrementali
- snapshot della knowledge base
- esportazione del vault
- esportazione del database
- ripristino selettivo
- rollback su modifiche automatiche
- verifica consistenza post-ripristino

---

## 26. Sicurezza, privacy e controllo

Se il sistema usa modelli remoti:
- separare dati sensibili
- supportare redazione automatica
- loggare i dati inviati fuori
- permettere esclusione di cartelle o note dall’elaborazione remota

Se il sistema usa modelli locali:
- gestire code, memoria e fallback

In ogni caso:
- l’utente deve mantenere controllo su dati, esportazione e cancellazione

---

## 27. Performance e ottimizzazione

Il sistema deve essere progettato per essere rapido.

Strategie richieste:
- caching query frequenti
- caching embedding
- incremental indexing
- retrieval multi-stage
- prefiltri prima del semantic search
- contesto minimale ma sufficiente
- uso di modelli diversi per compiti diversi
- evitare reprocessing completo quando non necessario

Obiettivo:
- percezione d’uso rapida
- latenza bassa nelle operazioni frequenti
- costo inferenziale controllato

---

## 28. Definition of Done dell’intero sistema

Il sistema è considerato riuscito solo se:

1. È possibile importare e organizzare contenuti eterogenei
2. È possibile fare query efficaci su memoria ibrida
3. Il sistema distingue tra archiviazione e conoscenza strutturata
4. Le informazioni rilevanti vengono promosse nella memoria attiva/strategica
5. L’utente può seguire progetti, decisioni e concetti nel tempo
6. Le risposte sono motivate da fonti interne tracciabili
7. Le modifiche automatiche sono auditabili e reversibili
8. Il sistema migliora progressivamente in base all’uso
9. L’architettura resta modulare e provider-agnostic
10. Il contenuto principale resta leggibile anche senza il motore AI

---

## 29. Roadmap obbligatoria di sviluppo

L’AI che implementa il progetto deve suddividere il lavoro in fasi.

### Fase 1 — Core minimo funzionante
- struttura cartelle
- database base
- import markdown
- indicizzazione base
- chat + retrieval
- note e progetti
- audit minimo

### Fase 2 — Memoria evolutiva
- scoring memoria
- memoria attiva/strategica/storica
- consolidamento periodico
- deduplica avanzata
- dashboard memoria

### Fase 3 — Knowledge graph e adattamento
- relazioni complesse
- adaptive ranking
- feedback learning
- explorer grafico
- project co-pilot

### Fase 4 — Sistema maturo
- multi-model routing
- job intelligenti
- controllo qualità avanzato
- reflection mode
- report evolutivi
- hardening completo

---

## 30. Output atteso dall’AI costruttrice

L’AI a cui viene fornito questo file deve produrre:

1. architettura tecnica completa
2. struttura cartelle iniziale
3. schema database
4. schema dei modelli dati
5. design del vector indexing
6. design del grafo
7. orchestratore centrale
8. pipeline ingestione
9. pipeline consolidamento memoria
10. servizi API
11. interfaccia base
12. sistema di audit
13. scheduler
14. configurazione provider LLM astratta
15. piano di test
16. piano di estensione futura

---

## 31. Regole finali di implementazione

L’AI che sviluppa il sistema deve seguire queste istruzioni finali:

- non creare una demo finta
- non creare un semplice wrapper su chatbot
- non mettere tutta la logica nel prompt
- non dipendere interamente da un provider
- non usare solo ricerca vettoriale
- non trattare tutte le note allo stesso modo
- non aggiornare la knowledge base senza audit
- non sacrificare leggibilità per automazione
- non costruire un sistema opaco

Deve invece:
- costruire una vera infrastruttura cognitiva
- separare livelli e responsabilità
- garantire controllo, memoria, evoluzione e velocità
- usare l’intelligenza artificiale come modulo di alto valore, non come stampella universale

---

## 32. Richiesta esecutiva finale da dare all’AI

Costruisci un sistema completo, reale e modulare di secondo cervello evolutivo chiamato **EvoBrain**, seguendo integralmente questa specifica.  
Il risultato deve essere una piattaforma cognitiva esterna capace di acquisire, organizzare, comprendere, collegare, consolidare, ricordare e adattarsi nel tempo.

La priorità assoluta è ottenere una struttura:
- superintelligente nell’uso della conoscenza
- intuitiva nell’interazione
- dinamica nella memoria
- evolutiva nel comportamento
- adattabile ai contesti
- rapida nell’operatività
- controllabile e verificabile in ogni sua parte

L’implementazione deve essere concreta, estendibile e pronta per crescita reale.
