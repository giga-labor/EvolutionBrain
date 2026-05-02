---
doc_id: evobrain-ui-modalita-azione-ai
title: EvoBrain - UI, Interazione Utente e Modalita di Azione dell'AI
version: 1.1.0
updated_at: 2026-04-27
status: authoritative
authority_level: L3
domain: ui
extends:
  - evobrain_specifica_definitiva_integrata.md
  - evobrain_modalita_operative_reali.md
replaces: []
---
# EvoBrain - UI, Interazione Utente e Modalita di Azione dell'AI
## Specifica dettagliata delle interfacce, dei flussi di interazione e dei comportamenti attivi dell'intelligenza

## 1. Scopo del documento

Definire:

- interfacce principali e secondarie
- flussi utente -> sistema -> azione
- modalita di azione visibile/invisibile dell'AI
- regole di conferma e supervisione per azioni sensibili
- criteri di trasparenza verso utente e audit

# 2. Principio guida della UI

La UI di EvoBrain deve rispettare questo principio:

**L’utente non deve interagire con un modello isolato, ma con una infrastruttura cognitiva trasparente.**

Questo implica che la UI deve mostrare chiaramente:

- cosa è stato recuperato
- da dove viene la risposta
- cosa è certo e cosa no
- se il sistema ha solo risposto o anche modificato qualcosa
- se un’azione è stata eseguita, proposta o simulata
- quale memoria o progetto è attualmente in focus

La UI non deve essere “magica” nel senso opaco del termine.  
Deve essere potente, ma leggibile.

---

# 3. Macro-famiglie di interazione utente

EvoBrain deve supportare almeno queste famiglie di interazione:

## 3.1 Interazione conversazionale
L’utente scrive o parla in linguaggio naturale e riceve risposte, sintesi, confronti, spiegazioni, proposte o azioni.

## 3.2 Interazione esplorativa
L’utente naviga tra note, concetti, grafo, progetti, timeline, episodi e procedure.

## 3.3 Interazione operativa
L’utente impartisce comandi espliciti o semiespliciti:
- crea
- aggiorna
- collega
- trasforma
- archivia
- pianifica
- confronta
- verifica

## 3.4 Interazione di supervisione
L’utente controlla:
- stato sistema
- stato job
- audit
- anomalie
- drift
- proposte di merge o consolidamento
- attività automatiche

## 3.5 Interazione riflessiva
L’utente usa il sistema per osservare:
- temi ricorrenti
- priorità
- evoluzione dei progetti
- pattern cognitivi
- contraddizioni
- cambiamenti nel tempo

---

# 4. Modalità UI principali

## 4.1 Chat Cognitiva Principale

### Scopo
Essere il punto di accesso più naturale al sistema.

### Funzioni
- domande in linguaggio naturale
- retrieval e spiegazione
- sintesi
- confronto tra idee
- analisi progetto
- trasformazione di testo in oggetti cognitivi
- azioni assistite
- reasoning su materiale interno

### Elementi UI minimi
- area input
- area output
- indicatori modalità attiva
- badge fonti usate
- badge epistemici
- badge stato risposta
- sezione “azioni suggerite”
- sezione “oggetti toccati”
- sezione “contesto attivo”

### Informazioni da mostrare nella risposta
- tipo di risposta
- fonti interne utilizzate
- livello di confidenza
- stato epistemico
- eventuali azioni eseguite o proposte
- eventuali conflitti rilevati

### Esempi di intenti
- “cosa avevo deciso su X?”
- “riassumi tutto sul progetto Y”
- “trasforma questa nota in task”
- “ci sono contraddizioni tra queste due idee?”
- “dammi una vista strategica di questo materiale”

---

## 4.2 Search & Retrieval Console

### Scopo
Permettere ricerca avanzata anche senza passare sempre dalla chat.

### Supporto richiesto
- ricerca per keyword
- ricerca full-text
- ricerca semantica
- ricerca per tag
- ricerca per tipo oggetto
- ricerca per progetto
- ricerca per data
- ricerca per stato
- ricerca per confidenza
- ricerca per relazioni

### Filtri UI
- note
- concetti
- decisioni
- task
- episodi
- procedure
- evidenze
- ipotesi
- progetti
- scenari
- preferenze

### Output
- lista risultati
- anteprima
- punteggio
- tipo oggetto
- livello di rilevanza
- provenienza memoria
- stato epistemico
- azioni rapide

### Azioni rapide per risultato
- apri
- confronta
- collega
- aggiungi a contesto
- pin
- archivia
- marca importante
- invia a chat

---

## 4.3 Knowledge Explorer

### Scopo
Navigare la conoscenza come struttura e non solo come testo.

### Funzioni
- vedere concetti e relazioni
- vedere cluster
- esplorare collegamenti
- vedere da quali note nasce un concetto
- vedere quali progetti lo usano
- vedere evidenze e conflitti

### UI minima
- nodo centrale selezionato
- relazioni in ingresso/uscita
- pannello dettaglio nodo
- timeline delle modifiche
- evidenze collegate
- stato validazione
- densità relazionale

### Modalità di navigazione
- per vicinanza semantica
- per relazioni dichiarate
- per progetto
- per centralità
- per conflitto
- per crescita recente

---

## 4.4 Graph View

### Scopo
Mostrare la struttura relazionale della memoria.

### Tipi di nodi visualizzabili
- concetti
- note
- decisioni
- obiettivi
- progetti
- persone
- evidenze
- ipotesi
- scenari
- episodi

### Tipi di archi
- related_to
- supports
- contradicts
- depends_on
- belongs_to
- derives_from
- extends
- unresolved_with
- decided_by
- evidence_for

### Funzioni
- zoom
- filtro per tipo relazione
- filtro per progetto
- filtro per confidenza
- evidenzia cluster
- evidenzia conflitti
- evidenzia percorsi tra due nodi
- invio selezione alla chat

---

## 4.5 Project Workspace

### Scopo
Dare a ogni progetto uno spazio operativo vivo.

### Contenuti minimi
- scopo
- stato
- obiettivi
- vincoli
- task
- decisioni
- timeline
- note collegate
- concetti principali
- problemi aperti
- prossime azioni
- episodi rilevanti

### Funzioni
- aggiornamento rapido stato
- aggiunta nota al progetto
- registrazione decisione
- creazione task
- vista cronologica
- riepilogo AI
- scansione incoerenze di progetto
- vista strategica

---

## 4.6 Decision Console

### Scopo
Tracciare decisioni, motivazioni e conseguenze.

### Campi minimi
- decisione
- data
- contesto
- progetto
- motivazioni
- evidenze
- alternative considerate
- rischio
- confidenza
- esito previsto
- revisione futura

### Funzioni
- aggiungi decisione
- collega a fonti
- collega a task
- collega a scenario
- marca da riesaminare
- verifica conseguenze dopo tempo

---

## 4.7 Memory Dashboard

### Scopo
Visualizzare il comportamento della memoria interna.

### Mostrare almeno
- memoria attiva corrente
- elementi in crescita
- elementi in decadenza
- promozioni recenti
- declassamenti recenti
- conflitti aperti
- concetti emergenti
- aree trascurate
- materiali da validare

### Utility
Questa dashboard serve a far capire che il sistema non è statico.

---

## 4.8 Audit & Control Panel

### Scopo
Permettere controllo reale e fiducia operativa.

### Mostrare almeno
- job recenti
- modifiche automatiche
- proposte in attesa
- errori
- retry
- rollback disponibili
- operazioni critiche
- azioni eseguite dall’AI
- livello di autonomia corrente
- modalità attiva del sistema

### Azioni utente
- approva
- rifiuta
- annulla
- riavvia job
- forza modalità safe
- cambia livello autonomia
- apri log dettagliato

---

## 4.9 Metacognitive Dashboard

### Scopo
Mostrare come il sistema valuta sé stesso.

### Mostrare almeno
- carico cognitivo stimato
- qualità retrieval
- qualità contesto
- rischio overconfidence
- query con contesto insufficiente
- drift rilevato
- qualità media delle risposte
- aree di debolezza attuali
- moduli in fallback

---

## 4.10 Operational Self Dashboard

### Scopo
Rendere visibile il modello del Sé operativo.

### Mostrare almeno
- ruolo attuale
- capacità attive
- capacità limitate o disabilitate
- focus corrente
- stato operativo
- livello autonomia
- livello di fiducia interna
- limiti attivi
- problemi recenti
- ultimo adattamento significativo

---

## 4.11 Scenario & Simulation View

### Scopo
Permettere all’utente di usare la simulazione interna in modo separato dal sapere consolidato.

### Funzioni
- definire premessa
- definire vincoli
- definire alternative
- lanciare simulazione
- confrontare scenari
- salvare scenari
- collegare scenario a decisioni e progetti

### Vincolo forte
Tutto ciò che è scenario deve essere visivamente separato dal contenuto consolidato.

---

## 4.12 Daily / Weekly Review View

### Scopo
Mostrare una sintesi temporale strutturata.

### Contenuti
- cosa è emerso
- cosa è stato deciso
- cosa resta aperto
- cosa è cresciuto
- cosa è decaduto
- blocchi
- progetti caldi
- idee ricorrenti
- task incompleti

---

# 5. Modalità UI secondarie

## 5.1 Quick Capture Bar
Per inserire un pensiero in pochi secondi.

## 5.2 Command Palette
Per azioni rapide:
- crea nota
- crea task
- collega a progetto
- cerca concetto
- apri dashboard
- lancia consolidamento
- safe mode

## 5.3 Context Tray
Mostra cosa è attualmente nel contesto della chat o del focus.

## 5.4 Side Inspector
Pannello laterale per vedere dettagli dell’oggetto selezionato.

## 5.5 Action Confirmation Modal
Conferma azioni sensibili.

## 5.6 Toast / Event Feed
Mostra eventi rapidi:
- nota acquisita
- job completato
- conflitto rilevato
- consolidamento proposto
- fallback attivato

---

# 6. Modello di interazione fondamentale

## 6.1 Flusso base query cognitiva
1. input utente
2. classificazione intento
3. selezione modalità
4. pianificazione retrieval
5. recupero dati interni
6. ranking
7. costruzione contesto
8. reasoning/generazione
9. etichettatura epistemica
10. presentazione UI
11. eventuale proposta di azione
12. eventuale aggiornamento memoria sessione

## 6.2 Flusso base comando operativo
1. input utente
2. riconoscimento comando/azione
3. individuazione oggetti target
4. verifica permessi/autonomia
5. simulazione a secco se richiesta
6. esecuzione o proposta
7. audit
8. feedback visivo

## 6.3 Flusso base navigazione esplorativa
1. selezione oggetto
2. caricamento dettaglio
3. recupero relazioni
4. visualizzazione
5. azioni contestuali
6. eventuale invio a chat o progetto

---

# 7. Modalità di azione dell’AI

L’AI non deve solo rispondere. Deve poter agire secondo modalità differenti.

## 7.1 Azione descrittiva
L’AI spiega, riassume, confronta, chiarisce.

## 7.2 Azione estrattiva
L’AI estrae:
- concetti
- task
- decisioni
- evidenze
- vincoli
- pattern
- entità

## 7.3 Azione organizzativa
L’AI:
- classifica
- collega
- tagga
- propone merge
- aggiorna stati
- ordina priorità

## 7.4 Azione trasformativa
L’AI converte materiale da una forma a un’altra:
- nota → task
- note sparse → sintesi
- testo grezzo → decisione
- discussione → progetto strutturato
- idee → piano operativo

## 7.5 Azione esplorativa
L’AI cerca relazioni, conflitti, buchi, ricorrenze, connessioni nascoste.

## 7.6 Azione propositiva
L’AI suggerisce:
- prossimi passi
- collegamenti
- task
- priorità
- revisioni
- scenari

## 7.7 Azione esecutiva
L’AI esegue realmente operazioni sul sistema:
- crea nota
- aggiorna progetto
- crea task
- collega oggetti
- archivia
- avvia job
- genera report

## 7.8 Azione simulativa
L’AI costruisce scenari, alternative, conseguenze.

## 7.9 Azione critica
L’AI evidenzia problemi, contraddizioni, debolezze, incertezze.

## 7.10 Azione metacognitiva
L’AI valuta la qualità del proprio operato, del contesto e del ragionamento.

---

# 8. Classi di azione AI per livello di impatto

## 8.1 Azioni a impatto nullo
Non modificano nulla.
Esempi:
- rispondi
- riassumi
- spiega
- confronta

## 8.2 Azioni a impatto basso
Modifiche locali, reversibili, non critiche.
Esempi:
- tag automatico
- classificazione
- aggiunta a contesto sessione
- pin temporaneo

## 8.3 Azioni a impatto medio
Modifiche persistenti ma non strategiche.
Esempi:
- creazione task
- creazione nota
- collegamento tra oggetti
- aggiornamento stato secondario

## 8.4 Azioni a impatto alto
Modificano la struttura cognitiva o strategica.
Esempi:
- merge concetti
- declassamento memoria
- promozione a memoria strategica
- modifica obiettivi
- archiviazione importante

## 8.5 Azioni a impatto critico
Richiedono quasi sempre validazione esplicita.
Esempi:
- cancellazione
- override strutturale
- modifica massiva
- reset di punteggi
- pruning aggressivo

---

# 9. Regole UI per la visibilità delle azioni AI

Ogni azione AI deve essere visivamente classificata come:

- **solo risposta**
- **suggerimento**
- **proposta di modifica**
- **simulazione**
- **azione eseguita**
- **azione fallita**
- **azione in attesa di conferma**
- **azione annullabile**

La UI deve mostrare chiaramente:
- cosa è successo
- su quali oggetti
- con quale confidenza
- se è reversibile
- chi l’ha autorizzata

---

# 10. Modello dei permessi e delle conferme

## 10.1 Regola generale
Più alta è la profondità di impatto, più forte deve essere il controllo umano, salvo policy esplicite.

## 10.2 Matrice minima

### Nessuna conferma richiesta
- Q&A
- sintesi
- ricerca
- analisi
- classificazione debole in sessione

### Conferma leggera
- crea nota
- crea task
- collega oggetti
- aggiorna stato non strategico

### Conferma forte
- merge concetti
- promozione strategica
- archiviazione importante
- modifica goal
- modifica self-model
- modifica pesi adattivi critici

### Conferma obbligatoria
- cancellazione
- reset
- pruning esteso
- override ad alto rischio
- azioni con impatto critico su conoscenza centrale

---

# 11. Modalità di input utente

## 11.1 Testo libero
Input principale.

## 11.2 Comandi naturali
Esempi:
- “trasforma questo in task”
- “salva come decisione”
- “collega al progetto X”
- “simula due alternative”

## 11.3 Comandi strutturati
Sintassi più precisa, per utenti avanzati.

## 11.4 Drag and drop
Per file, documenti, appunti.

## 11.5 Selezione multipla UI
Per confronti, merge, tagging, collegamenti.

## 11.6 Voce
Opzionale, con trascrizione.

---

# 12. Modalità di output AI

## 12.1 Risposta testuale semplice
Per query rapide.

## 12.2 Risposta strutturata
Con sezioni:
- sintesi
- fonti
- conflitti
- azioni suggerite

## 12.3 Risposta operativa
Con bottoni o azioni:
- crea
- salva
- collega
- apri
- conferma

## 12.4 Risposta comparativa
Confronto tra idee, note, scenari, decisioni.

## 12.5 Risposta grafica / relazionale
Via knowledge explorer o grafo.

## 12.6 Risposta temporale
Via timeline o review.

---

# 13. Modello di contesto visibile all’utente

L’utente deve poter vedere sempre almeno una parte del contesto attivo.

## 13.1 Contesto chat
- progetto attivo
- note pin
- oggetti selezionati
- memoria usata
- modalità attiva

## 13.2 Contesto progetto
- obiettivi in focus
- decisioni recenti
- task aperti
- blocchi

## 13.3 Contesto cognitivo
- concetti centrali
- conflitti aperti
- piste attive
- scenari in valutazione

---

# 14. UI per fonti interne ed esterne

Il sistema deve distinguere visivamente l’origine delle informazioni.

## 14.1 Fonti interne
- note
- DB
- memoria
- progetti
- episodi
- procedure
- grafo
- audit

## 14.2 Fonti esterne
- web
- connettori
- documenti remoti
- servizi esterni autorizzati

## 14.3 Regola
La UI deve indicare sempre:
- fonte interna
- fonte esterna
- inferenza
- scenario
- contenuto non verificato

---

# 15. Policy UI sul web e sulle fonti esterne

Default:
- web disattivato
- solo fonti interne

Modalità alternative:
- web su richiesta esplicita
- web su workspace dedicato
- web su policy configurata

La UI deve mostrare chiaramente:
- quando è entrato materiale esterno
- se una risposta usa materiale esterno
- se il sistema sta lavorando solo sulla memoria interna

---

# 16. Modalità di lavoro AI invisibili ma controllabili

Esistono azioni non sempre visibili in primo piano, ma ispezionabili.

## 16.1 Queue processing
## 16.2 Indicizzazione incrementale
## 16.3 Consolidamento leggero
## 16.4 Rebuild indici
## 16.5 Contradiction scan
## 16.6 Aggiornamento scoring memoria
## 16.7 Refresh dashboard
## 16.8 Adattamento ranking
## 16.9 Monitoraggio health
## 16.10 Backup

Tutte devono comparire almeno in audit e job console.

---

# 17. UI per stati e modalità del sistema

Il sistema deve mostrare in modo compatto e chiaro:
- idle
- capturing
- processing
- reasoning
- consolidating
- maintaining
- degraded
- safe_mode
- error_state

E deve mostrare anche:
- profilo inferenziale corrente
- autonomia corrente
- progetto attivo
- focus cognitivo
- coda lavori

---

# 18. Modalità di supervisione umana

L’utente deve poter:

- approvare proposte
- respingere merge
- correggere concetti
- bloccare fonti
- disabilitare moduli
- abbassare autonomia
- forzare safe mode
- lanciare rollback
- marcare una risposta come errata o utile
- imporre priorità a un progetto
- congelare una parte della knowledge base

---

# 19. Error UX e comportamenti di fallback

Quando qualcosa fallisce, la UI non deve nascondere.

Deve dire:
- cosa ha fallito
- dove ha fallito
- cosa è rimasto intatto
- cosa si può fare ora
- se esiste un fallback

### Esempi
- “Il modello principale non è disponibile. Uso retrieval interno senza sintesi avanzata.”
- “Indicizzazione parziale completata. Alcuni chunk saranno reprocessati.”
- “Merge non eseguito: confidenza troppo bassa.”

---

# 20. Principi UX fondamentali

1. chiarezza prima di spettacolo  
2. trasparenza prima di magia  
3. controllo prima di autonomia aggressiva  
4. velocità nelle operazioni comuni  
5. profondità disponibile su richiesta  
6. distinzione netta tra sapere, ipotizzare, simulare e agire  
7. ridurre il carico cognitivo dell’utente, non aumentarlo  
8. ogni vista deve avere una utilità reale  
9. nessun pannello deve essere solo ornamentale  
10. la chat non deve soffocare la navigazione strutturata

---

# 21. Definition of Done per UI e azione AI

La componente UI/UX e azione AI è completa solo se:

1. l’utente può usare EvoBrain senza conoscere l’architettura interna
2. la chat è potente ma non opaca
3. esiste ricerca avanzata reale
4. esistono viste strutturate per memoria, progetti, grafo, audit e simulazione
5. l’AI distingue chiaramente risposta, suggerimento, simulazione e azione
6. le azioni sensibili richiedono controlli adeguati
7. l’utente può vedere sempre cosa il sistema sta facendo
8. l’origine delle informazioni è sempre chiara
9. l’utente può supervisionare e correggere la AI
10. il sistema resta rapido e comprensibile anche quando cresce

---

# 22. Istruzione esecutiva finale

Implementa l’intero livello di **interazione utente, UI operativa e modalità di azione dell’AI** per EvoBrain seguendo integralmente questo documento.

La UI non deve essere un contorno grafico di un chatbot.  
Deve essere il punto di accesso reale a una infrastruttura cognitiva complessa, ma usabile.

L’AI non deve solo parlare: deve poter cercare, organizzare, proporre, simulare, aggiornare, eseguire, fermarsi, chiedere conferma, spiegare cosa ha fatto e mostrare sempre il confine tra memoria, inferenza, scenario e azione.

Costruisci una interfaccia e un sistema di azione in cui l’utente abbia sempre:
- potenza
- leggibilità
- controllo
- velocità
- profondità
- fiducia operativa
