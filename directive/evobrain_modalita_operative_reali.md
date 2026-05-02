---
doc_id: evobrain-modalita-operative-reali
title: EvoBrain - Modalita operative reali
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L3
domain: operations
extends:
  - evobrain_specifica_definitiva_integrata.md
replaces: []
---
# Modalita operative reali di EvoBrain
## Documento operativo collegato alla specifica architetturale principale

## 1. Scopo di questo documento

Definire in modo operativo:

- modalita runtime supportate dal sistema
- regole di transizione tra modalita
- livello di autonomia ammesso per ogni contesto
- gestione costo/latenza/rischio
- criteri di fallback e safe mode

## 2. Principio operativo generale

EvoBrain deve funzionare come una **piattaforma cognitiva esterna multi-modalità**, capace di assumere comportamenti differenti in base a:

- tipo di input
- urgenza
- importanza
- affidabilità delle fonti
- contesto attuale
- progetto attivo
- livello di energia computazionale disponibile
- disponibilità o meno di modelli locali/remoti
- livello di autonomia consentito

Il sistema **non deve comportarsi sempre allo stesso modo**.

Deve invece scegliere dinamicamente la modalità più adatta.

---

## 3. Assi decisionali che governano il comportamento

Ogni azione del sistema deve essere regolata almeno da questi assi:

### 3.1 Asse del tempo
- real-time
- near-real-time
- batch
- periodico
- differito

### 3.2 Asse dell’autonomia
- manuale
- assistita
- semi-automatica
- automatica con verifica
- automatica autonoma controllata

### 3.3 Asse epistemico
- dato grezzo
- dato verificato
- inferenza
- ipotesi
- suggerimento
- decisione consolidata

### 3.4 Asse della memoria
- volatile
- temporanea
- attiva
- contestuale
- strategica
- storica
- latente

### 3.5 Asse del costo inferenziale
- zero-LLM
- low-cost inference
- normal inference
- deep reasoning
- consolidation batch

### 3.6 Asse del rischio
- rischio basso
- rischio medio
- rischio alto
- rischio critico

---

## 4. Modalità operative principali

EvoBrain deve supportare almeno le seguenti modalità reali.

## 4.1 Modalità Capture Passiva

### Scopo
Assorbire contenuti senza interrompere l’utente, con intervento minimo.

### Quando si attiva
- nuova nota rapida
- file inserito in cartella monitorata
- testo incollato
- import automatico da fonti abilitate
- trascrizione appena generata
- salvataggio rapido da web o appunto

### Comportamento
- acquisisce il contenuto
- calcola hash
- crea record sorgente
- aggiunge metadati minimi
- assegna stato `raw_pending`
- mette il contenuto in coda per normalizzazione
- non disturba l’utente salvo errore critico

### Componenti attive
- ingestion layer
- storage raw
- job queue
- audit minimo

### Vincoli
- latenza molto bassa
- niente ragionamenti costosi
- niente inferenze profonde immediate
- priorità alla robustezza dell’acquisizione

### Output
- contenuto catturato
- job registrato
- log evento

---

## 4.2 Modalità Ingestione Attiva

### Scopo
Elaborare uno o più contenuti appena acquisiti per renderli utili al sistema.

### Quando si attiva
- on-demand
- dopo capture passiva
- in finestre batch
- su comando utente “processa tutto”

### Comportamento
- parsing del documento
- normalizzazione
- pulizia
- chunking
- classificazione
- estrazione metadati
- stima qualità del contenuto
- salvataggio in memoria elaborata

### Componenti attive
- normalization layer
- parser
- content classifier
- metadata extractor
- dedupe checker
- chunker

### Output
- documento normalizzato
- chunk persistiti
- qualità stimata
- tipo contenuto assegnato

---

## 4.3 Modalità Analisi Semantica

### Scopo
Trasformare contenuti normalizzati in materiale semanticamente navigabile.

### Quando si attiva
- dopo normalizzazione
- on-demand
- batch notturno
- aggiornamento knowledge layer

### Comportamento
- genera embedding
- aggiorna indice vettoriale
- aggiorna indice lessicale
- estrae entità
- estrae concetti candidati
- propone relazioni candidate
- aggiorna cluster semantici

### Componenti attive
- semantic layer
- vector encoder
- lexical indexer
- entity linker
- relation extractor
- concept miner

### Output
- contenuto semanticamente indicizzato
- entità candidate
- concetti candidati
- relazioni candidate

---

## 4.4 Modalità Consolidamento della Conoscenza

### Scopo
Trasformare materiale disperso in conoscenza strutturata persistente.

### Quando si attiva
- batch periodico
- su progetto specifico
- su richiesta dell’utente
- dopo accumulo di nuove informazioni su uno stesso tema

### Comportamento
- aggrega evidenze
- confronta nuovi concetti con concetti esistenti
- fonde duplicati concettuali
- aggiorna oggetti cognitivi
- promuove elementi rilevanti
- rileva contraddizioni
- produce snapshot evolutivo

### Componenti attive
- knowledge layer
- memory layer
- relation validator
- contradiction checker
- summarizer
- audit controller

### Output
- knowledge objects aggiornati
- promozione/declassamento memoria
- report di consolidamento

---

## 4.5 Modalità Chat Operativa

### Scopo
Interagire in linguaggio naturale con l’utente usando il sistema come memoria e motore cognitivo.

### Quando si attiva
- query utente
- comando naturale
- richiesta di ricerca, sintesi, confronto, pianificazione

### Comportamento
- classifica l’intento
- determina il task type
- cerca in memoria strutturata
- esegue retrieval lessicale + semantico + grafo
- costruisce contesto
- decide livello inferenziale
- produce risposta
- opzionalmente aggiorna memoria sessione

### Sotto-modalità interne
- Q&A semplice
- ricerca mirata
- confronto concettuale
- sintesi multi-fonte
- analisi progetto
- trasformazione in task
- revisione critica

### Componenti attive
- orchestratore
- retriever ibrido
- ranking engine
- reasoning layer
- response builder
- memory session updater

### Output
- risposta motivata
- link alle fonti interne
- eventuali azioni proposte o eseguite

---

## 4.6 Modalità Project Co-Pilot

### Scopo
Seguire un progetto nel tempo come supporto cognitivo e operativo persistente.

### Quando si attiva
- l’utente apre un progetto
- query legate a un progetto
- scheduler su progetto attivo
- rilevazione di nuova attività sul progetto

### Comportamento
- attiva contesto progetto
- carica obiettivi, vincoli, task, decisioni, note, timeline
- aggiorna priorità
- rileva blocchi o incoerenze
- suggerisce prossimi passi
- registra nuove decisioni
- collega tutto al progetto

### Componenti attive
- project context engine
- memory layer
- reasoning layer
- task mapper
- timeline builder
- audit layer

### Output
- stato progetto aggiornato
- task collegati
- decision log
- riepilogo operativo

---

## 4.7 Modalità Research

### Scopo
Analizzare un argomento, raccogliere materiale, confrontarlo e costruire una mappa concettuale utile.

### Quando si attiva
- richiesta di studio
- richiesta di confronto tra idee
- investigazione su tema complesso
- costruzione di dossier o base conoscitiva

### Comportamento
- definisce perimetro dell’indagine
- raccoglie materiale interno rilevante
- ordina le fonti
- costruisce cluster tematici
- evidenzia concordanze e conflitti
- crea una sintesi stratificata
- propone domande aperte

### Componenti attive
- retriever ibrido
- cluster engine
- contradiction checker
- concept graph explorer
- summarizer
- report builder

### Output
- dossier sintetico
- mappa concettuale
- evidenze
- conflitti
- temi emergenti
- domande aperte

---

## 4.8 Modalità Reflection

### Scopo
Consentire al sistema di riflettere sul proprio contenuto, sulle priorità e sulle traiettorie cognitive.

### Quando si attiva
- schedulata
- su richiesta utente
- in assenza di attività urgente
- dopo grandi quantità di nuovo materiale

### Comportamento
- analizza temi più frequenti
- rileva aree ad alta densità semantica
- individua contraddizioni aperte
- identifica ciò che cresce e ciò che decade
- aggiorna centralità concettuale
- propone riequilibrio della memoria
- produce report metacognitivo

### Componenti attive
- memory analyzer
- semantic graph analyzer
- adaptation engine
- summary engine
- audit logger

### Output
- report di riflessione
- candidati promozione/declassamento
- concetti emergenti
- punti ciechi del sistema

---

## 4.9 Modalità Maintenance

### Scopo
Mantenere ordine, integrità e prestazioni.

### Quando si attiva
- pianificata
- manuale
- in caso di degrado
- dopo errori o aggiornamenti di schema

### Comportamento
- verifica integrità file e database
- ricostruisce indici se necessario
- pulisce cache
- verifica orfani relazionali
- testa consistenza embeddings registry
- controlla jobs bloccati
- produce report salute sistema

### Componenti attive
- scheduler
- integrity checker
- index manager
- db maintenance manager
- vector maintenance manager
- log inspector

### Output
- stato salute
- problemi individuati
- azioni correttive
- report manutenzione

---

## 4.10 Modalità Safe Mode

### Scopo
Ridurre il sistema a una modalità controllata in caso di guasti, rischio alto o comportamento anomalo.

### Quando si attiva
- errore grave
- integrità compromessa
- provider LLM non disponibili
- risultati altamente incoerenti
- superamento soglie di rischio

### Comportamento
- blocca aggiornamenti automatici critici
- disattiva inferenze profonde non necessarie
- consente retrieval e consultazione di base
- richiede validazione umana per modifiche sensibili
- aumenta il logging
- abbassa il livello di autonomia

### Componenti attive
- orchestratore in profilo restrittivo
- retrieval base
- audit massimo
- safe policy engine

### Output
- sistema ridotto ma utilizzabile
- allerta interna
- report anomalia

---

## 5. Modalità operative secondarie e specialistiche

## 5.1 Modalità Quick Note
Pensata per catturare un pensiero in pochi secondi.

Comportamento:
- crea nota minima
- assegna timestamp
- inferisce tipo solo se molto probabile
- evita elaborazioni pesanti immediate
- mette in coda per arricchimento successivo

## 5.2 Modalità Daily Review
Costruisce una sintesi giornaliera di attività, note, decisioni e priorità.

## 5.3 Modalità Weekly Synthesis
Unisce la settimana in una vista più consolidata:
- temi
- progressi
- blocchi
- ricorrenze
- concetti cresciuti
- task aperti

## 5.4 Modalità Decision Tracking
Focalizzata su decisioni prese, motivazioni, fonti, conseguenze e revisione futura.

## 5.5 Modalità Contradiction Scan
Scandisce base conoscitiva e note recenti per individuare elementi incompatibili.

## 5.6 Modalità Learning from Feedback
Elabora i feedback dell’utente e aggiorna pesi, ranking e comportamenti del sistema.

## 5.7 Modalità Archive Compression
Riduce il rumore dell’archivio:
- compatta materiale ridondante
- sintetizza vecchi cluster
- preserva fonti
- riduce dispersione

---

## 6. Motore di selezione della modalità

Il sistema deve avere un **Mode Selection Engine** che scelga la modalità operativa corretta.

### Input del selettore
- tipo di evento
- origine evento
- contenuto
- livello urgenza
- progetto coinvolto
- energia computazionale disponibile
- stato attuale sistema
- profilo autonomia
- rischio
- disponibilità modelli
- coda lavori

### Output del selettore
- modalità primaria
- eventuale sotto-modalità
- profilo di costo
- profilo di audit
- eventuale fallback

### Regola fondamentale
La modalità selezionata deve essere **la meno costosa e più sicura** che consenta comunque di completare bene il compito.

---

## 7. Stati operativi del sistema

EvoBrain deve mantenere uno stato globale e stati locali.

## 7.1 Stato globale sistema
Valori minimi:
- booting
- idle
- capturing
- processing
- reasoning
- consolidating
- maintaining
- degraded
- safe_mode
- error_state

## 7.2 Stato dei job
Valori minimi:
- queued
- running
- paused
- retrying
- completed
- failed
- cancelled
- awaiting_validation

## 7.3 Stato degli oggetti cognitivi
Valori minimi:
- raw
- normalized
- indexed
- candidate
- validated
- active
- latent
- archived
- deprecated
- conflicted

---

## 8. Livelli di autonomia

Il sistema deve supportare livelli configurabili.

## 8.1 Livello 0 — Manuale puro
Il sistema non modifica nulla senza comando esplicito.

## 8.2 Livello 1 — Assistito
Il sistema propone ma non esegue aggiornamenti rilevanti.

## 8.3 Livello 2 — Semi-automatico
Il sistema esegue operazioni non critiche in autonomia e propone quelle sensibili.

## 8.4 Livello 3 — Automatico con verifica
Il sistema esegue quasi tutto, ma gli aggiornamenti critici richiedono validazione.

## 8.5 Livello 4 — Autonomia controllata
Il sistema esegue anche consolidamenti complessi entro limiti di rischio e audit stringente.

### Regola
Il livello massimo di autonomia deve essere configurabile per:
- tipo di progetto
- tipo di memoria
- tipo di azione
- rischio
- ambiente locale/remoto

---

## 9. Livelli di costo inferenziale

Per essere rapido ed efficiente, EvoBrain deve usare profili operativi di costo.

## 9.1 Zero-LLM Profile
Usa solo:
- database
- full-text
- regole
- scoring
- grafi
- template

## 9.2 Low Profile
Usa modelli piccoli o chiamate economiche per:
- classificazione
- tagging
- mini-sintesi

## 9.3 Standard Profile
Usa retrieval ibrido e modello principale per compiti normali.

## 9.4 Deep Profile
Usa modelli più forti e contesto più ricco per:
- confronto complesso
- sintesi strategica
- reflection
- consolidamento avanzato

## 9.5 Batch Deep Profile
Usato fuori dal realtime, in finestre dedicate, per operazioni costose e non urgenti.

---

## 10. Politica di priorità runtime

Ogni richiesta e job deve essere ordinato in base a priorità.

### Priorità assolute
1. integrità del sistema
2. salvataggio dati
3. operazioni richieste direttamente dall’utente
4. job bloccanti per esperienza utente
5. aggiornamento memoria attiva
6. consolidamenti programmati
7. manutenzione ordinaria
8. analisi profonde differibili

### Fattori di priorità
- urgenza
- rischio perdita dati
- coinvolgimento progetto attivo
- frequenza d’uso
- dipendenze di altri job
- finestra temporale ideale
- costo computazionale
- valore strategico

---

## 11. Flussi operativi reali principali

## 11.1 Flusso: nuova nota manuale
1. ricezione input
2. creazione nota grezza
3. assegnazione id
4. save immediato
5. metadati minimi
6. queue arricchimento
7. eventuale quick classification
8. update audit

## 11.2 Flusso: import documenti
1. scoperta file
2. hashing
3. duplicate check
4. parse
5. normalizzazione
6. chunking
7. indexing
8. extraction
9. candidate relations
10. knowledge update proposal
11. audit final

## 11.3 Flusso: domanda dell’utente
1. intent classification
2. mode selection
3. retrieval planning
4. search memoria strutturata
5. search lessicale
6. search semantica
7. search grafo
8. ranking
9. context assembly
10. reasoning/generation
11. epistemic labeling
12. answer output
13. optional session memory update

## 11.4 Flusso: consolidamento notturno
1. raccogli nuovi contenuti
2. cluster per tema/progetto
3. fusione candidati duplicati
4. aggiorna concetti
5. ricalcola memory scores
6. promuovi/declassa
7. genera report
8. salva snapshot
9. audit completo

## 11.5 Flusso: feedback utente
1. ricezione feedback
2. classificazione feedback
3. localizzazione oggetto coinvolto
4. aggiornamento confidenza o ranking
5. log apprendimento
6. eventuale ricalibrazione modulo
7. audit

---

## 12. Policy di aggiornamento memoria

Il sistema deve applicare regole chiare.

### 12.1 Promozione memoria
Un contenuto può essere promosso se:
- richiamato spesso
- rilevante per progetto attivo
- collegato a decisioni
- confermato da più fonti interne
- segnato come importante dall’utente
- semanticamente centrale

### 12.2 Declassamento memoria
Un contenuto può essere declassato se:
- non consultato da molto
- non più collegato a progetti vivi
- basso peso strategico
- ridondante
- sostituito da versioni consolidate

### 12.3 Archiviazione
Un contenuto può essere archiviato se:
- storicamente utile ma non operativo
- già consolidato altrove
- concluso
- irrilevante nel breve/medio termine

### 12.4 Blocco promozione automatica
La promozione automatica deve essere bloccata per:
- contenuti ambigui
- relazioni deboli
- materiale contraddittorio
- evidenza insufficiente

---

## 13. Politica di verifica e validazione

Ogni aggiornamento strutturale importante deve passare almeno per uno di questi livelli:

### Livello A — Autovalidazione deterministica
Per operazioni come:
- hashing
- deduplica esatta
- rebuild indici
- metadati tecnici

### Livello B — Validazione euristica
Per operazioni come:
- classificazione
- scoring
- ranking
- clusterizzazione

### Livello C — Validazione semantica
Per:
- fusioni concettuali
- relazioni nuove
- sintesi persistenti
- aggiornamenti a conoscenza strategica

### Livello D — Validazione umana
Obbligatoria per:
- modifiche strategiche ad alta incertezza
- merge ambigui
- declassamenti importanti
- cancellazioni
- override profondi

---

## 14. Modalità di risposta del sistema verso l’utente

Il sistema deve saper rispondere in modalità differenti.

## 14.1 Modalità Informativa
Recupera e presenta dati e contenuti.

## 14.2 Modalità Sintetica
Riduce materiale in una forma compatta.

## 14.3 Modalità Analitica
Confronta, scompone, verifica, esplicita struttura e relazioni.

## 14.4 Modalità Operativa
Propone o crea task, piani, checklist, modifiche.

## 14.5 Modalità Critica
Rileva problemi, incoerenze, debolezze, lacune.

## 14.6 Modalità Strategica
Collega materiale a obiettivi, vincoli, priorità e traiettorie di lungo periodo.

---

## 15. Regole di persistenza e aggiornamento sessione

La sessione corrente deve avere una memoria locale temporanea.

### Deve conservare
- query recenti
- documenti consultati
- progetto attivo
- oggetti cognitivi centrali della sessione
- ipotesi operative temporanee
- ultimi suggerimenti generati
- feedback immediati

### Deve poter promuovere
- decisioni prese
- nuove preferenze confermate
- nuove note di progetto
- correzioni utili
- concetti stabilizzati

### Deve scadere
- contesto volatile non confermato
- ipotesi deboli
- transienti tecnici

---

## 16. Adattamento dinamico del comportamento

Il sistema deve imparare:
- quale tipo di risultati l’utente apre davvero
- quali sintesi sono considerate utili
- quali collegamenti vengono accettati
- quali suggerimenti vengono ignorati
- quali progetti dominano il periodo
- quale profondità di risposta è più efficace

### Effetti ammessi dell’adattamento
- migliore ranking
- diversa densità delle sintesi
- migliore routing dei task
- diversa aggressività di promozione memoria
- migliore selezione del contesto
- raffinamento dei pesi

### Effetti vietati
- cambiamenti opachi non loggati
- cancellazioni automatiche non auditabili
- drift incontrollato del comportamento

---

## 17. Regole di controllo delle allucinazioni operative

Per qualsiasi inferenza o collegamento nuovo:
- allegare evidence refs
- indicare confidenza
- etichettare come inferenza o ipotesi
- non consolidare automaticamente se debole
- verificare conflitti con base esistente
- permettere revisione

Per qualsiasi sintesi:
- mantenere riferimenti alle fonti interne
- non spacciare interpretazioni per fatti

Per qualsiasi suggerimento:
- separarlo dalla memoria consolidata

---

## 18. Gestione dei fallimenti

Il sistema deve prevedere fallimenti normali.

## 18.1 Fallimenti ingestione
Azioni:
- retry limitato
- quarantena file problematico
- log dettagliato
- nessuna perdita delle fonti sane

## 18.2 Fallimenti indicizzazione
Azioni:
- segna item come partially_processed
- consenti consultazione raw
- pianifica reprocessing

## 18.3 Fallimenti LLM
Azioni:
- fallback a modalità più semplice
- retrieval senza generazione
- riuso cache se disponibile
- audit errore provider

## 18.4 Fallimenti consolidamento
Azioni:
- rollback snapshot
- congelamento knowledge update
- richiesta verifica

## 18.5 Fallimenti di integrità
Azioni:
- attiva safe mode
- blocca scritture sensibili
- notifica
- produce report

---

## 19. Metriche operative che il sistema deve tracciare

### Metriche di ingestione
- numero contenuti acquisiti
- tasso errori
- tempo medio di parsing
- tasso deduplica

### Metriche di retrieval
- latenza query
- qualità top results
- click-through interno
- tasso consultazione fonti suggerite

### Metriche di memoria
- dimensione per layer
- promozioni/declassamenti
- tasso consolidamento
- numero conflitti aperti

### Metriche di adattamento
- feedback ricevuti
- suggerimenti accettati/rifiutati
- variazioni ranking
- accuratezza percepita

### Metriche di affidabilità
- rollback eseguiti
- errori critici
- tempo in safe mode
- numero operazioni con audit incompleto

### Metriche di costo
- chiamate LLM per tipo
- costo stimato
- cache hit rate
- % query risolte senza LLM

---

## 20. Scheduler operativo reale

Il sistema deve avere uno scheduler con priorità e finestre.

### Job frequenti
- queue processor
- indicizzazione incrementale
- refresh dashboard
- controllo jobs sospesi

### Job giornalieri
- daily review
- consolidamento leggero
- backup incrementale
- manutenzione cache

### Job settimanali
- weekly synthesis
- contradiction scan
- archive compression
- report evolutivo

### Job mensili
- re-evaluation strategica
- pulizia profonda
- stress test
- export snapshot

---

## 21. Profili d’uso reali

## 21.1 Profilo Archivista
Favorisce ordine, classificazione, precisione.

## 21.2 Profilo Thinker
Favorisce collegamenti, domande, concetti e riflessione.

## 21.3 Profilo Maker
Favorisce progetto, task, operatività e velocità.

## 21.4 Profilo Researcher
Favorisce profondità, fonti, mappe e confronto.

## 21.5 Profilo Hybrid
Bilanciato e adattivo.

Il sistema deve permettere di configurare profili iniziali e poi personalizzarli con l’uso.

---

## 22. Profili ambientali

## 22.1 Local-only
Tutto gira in locale, con massima privacy e autonomia.

## 22.2 Hybrid
Memoria e logica locale, alcuni modelli remoti.

## 22.3 Cloud-assisted
Più dipendenza da provider esterni ma maggiore potenza immediata.

Ogni modalità deve modificare:
- routing dei task
- livello di privacy
- costo
- fallback
- latenza attesa

---

## 23. Regole di audit operativo

Ogni azione significativa deve produrre almeno:
- timestamp
- actor
- mode
- action type
- target objects
- input refs
- output refs
- confidence
- status
- rollback available yes/no

L’audit deve essere:
- consultabile
- filtrabile
- persistente
- non alterabile silenziosamente

---

## 24. Definition of Done operativa

La parte operativa del sistema è considerata completa solo se:

1. il sistema sa scegliere la modalità corretta per ogni evento principale
2. ogni modalità ha comportamenti chiari, sicuri e tracciabili
3. i passaggi tra modalità sono governati da regole esplicite
4. il livello di autonomia è configurabile
5. il costo inferenziale è controllato
6. i fallimenti non compromettono dati o conoscenza
7. la memoria si aggiorna con regole verificabili
8. il sistema può lavorare in realtime e batch
9. esiste safe mode reale
10. l’intero comportamento runtime è auditabile

---

## 25. Istruzione esecutiva finale da dare all’AI costruttrice

Implementa il **motore operativo reale di EvoBrain** seguendo integralmente questo documento e la specifica architetturale principale.

Il sistema deve comportarsi come una struttura cognitiva esterna realmente utilizzabile, capace di scegliere modalità operative diverse in base a contesto, rischio, costo, priorità e tipo di compito.

Deve essere:
- rapido nelle operazioni frequenti
- profondo quando serve
- prudente nelle modifiche strutturali
- adattivo nel tempo
- affidabile nel salvataggio e nell’audit
- capace di alternare realtime, batch, consolidamento e riflessione

Non costruire una simulazione astratta del comportamento.  
Costruisci un motore operativo concreto, governato da stati, policy, livelli di autonomia, flussi reali, fallback, controlli e log.
