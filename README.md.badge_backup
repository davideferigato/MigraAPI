# 🦾 MigraAPI – Claude Agent per migrazione automatica di API

> Agente AI basato su **Claude Skills** e **Subagents** (Anthropic) che migra codice da vecchia API a nuova API in modo automatico, sicuro e scalabile.

## 📌 Indice
- [Introduzione](#introduzione)
- [Architettura](#architettura)
- [Come funziona la Progressive Disclosure](#come-funziona-la-progressive-disclosure)
- [Skills vs CLAUDE.md vs Hooks vs Subagents](#skills-vs-claudemd-vs-hooks-vs-subagents)
- [Prerequisiti](#prerequisiti)
- [Installazione](#installazione)
- [Come usare MigraAPI](#come-usare-migraapi)
- [Distribuzione come plugin](#distribuzione-come-plugin)
- [Enterprise Managed Settings](#enterprise-managed-settings)
- [Best practice di sicurezza](#best-practice-di-sicurezza)
- [Esempi](#esempi)
- [Troubleshooting](#troubleshooting)
- [Roadmap e contributi](#roadmap-e-contributi)
- [Licenza](#licenza)

## Introduzione

MigraAPI è un progetto dimostrativo che implementa i concetti avanzati di **Agent Skills** e **Subagents** insegnati nei corsi ufficiali di Anthropic. Permette di automatizzare la migrazione di chiamate API deprecate in codebase Python e JavaScript, usando un agente orchestratore che delega task a subagent specializzati in isolamento.

## Architettura

Il sistema segue il **pattern dell’orchestratore**:

```
Utente → Orchestratore (Claude Code) → Subagent scanner → Subagent rewriter → Subagent validator
                                        ↑                    ↑                    ↑
                                        (parallel on files)  (parallel)           (parallel)
```

### Componenti

1. **Skill `api-migration`**  
   - Contiene le regole di migrazione (mapping old → new), i pattern regex e lo script scanner.  
   - Segue il meccanismo di **progressive disclosure** (vedi sotto).

2. **Subagent `scanner`**  
   - Isolato, riceve un file e restituisce JSON con le occorrenze deprecate.  
   - Tool consentiti: solo lettura (`Read`, `Grep`, `Glob`).

3. **Subagent `rewriter`**  
   - Applica le trasformazioni usando le regole di mapping.  
   - Tool consentiti: `Read`, `Write`, `Edit`.

4. **Subagent `validator`**  
   - Verifica la correttezza sintattica (e opzionalmente esegue test).  
   - Restituisce JSON con esito e lista errori (obstacle reporting).

5. **Orchestratore**  
   - L’agente principale (Claude Code) carica la skill e coordina i subagent.  
   - Può eseguire i subagent in **parallelo** su più file per massimizzare l’efficienza.

## Come funziona la Progressive Disclosure

La progressive disclosure è un meccanismo a 3 livelli che ottimizza l’uso del contesto da parte di Claude:

| Livello | Descrizione |
|---------|-------------|
| **1. Discovery** | All’avvio, Claude pre-carica solo `name` e `description` della skill nel system prompt. Consumo di contesto minimo. |
| **2. Activation** | Quando il task corrente corrisponde alla descrizione (es. l’utente chiede di migrare un’API), Claude legge l’intero file `SKILL.md` (istruzioni, regole, esempi). |
| **3. Execution** | Se necessario, Claude carica file aggiuntivi (`migration-rules.json`, `regex-patterns.md`) ed esegue script esterni (`scanner.py`) che non consumano contesto aggiuntivo. |

**Vantaggi**: Skills complesse non appesantiscono il contesto in conversazioni generiche. Solo quando servono vengono caricate.

## Skills vs CLAUDE.md vs Hooks vs Subagents

Questa tabella confronta le principali funzionalità di Claude Code:

| Funzionalità | Scopo | Quando usarla | Esempio |
|--------------|-------|---------------|---------|
| **Skills** | Istruzioni dinamiche e riutilizzabili per task specializzati | Workflow ripetuti che richiedono conoscenza specifica (es. migrazione API) | `api-migration` skill con regole di trasformazione |
| **CLAUDE.md** | Configurazione generale del progetto (sempre attiva) | Impostazioni di progetto, preferenze di stile, comandi di build | Ignorare certi file, impostare variabili d’ambiente |
| **Hooks** | Automazioni basate su eventi (pre/post esecuzione) | Trigger automatici come “prima di ogni modifica, fai backup” | `pre-edit` hook che salva una copia del file |
| **Subagents** | Delegazione di task a context window isolate | Task che esploderebbero il contesto principale, esecuzione parallela | Scanner, rewriter, validator in isolamento |

**Perché le Skills sono più efficienti**: Consentono di insegnare una volta sola a Claude come fare un task complesso, senza ripetere istruzioni ogni volta. In combinazione con Subagents, si ottiene scalabilità e pulizia del contesto.

## Prerequisiti

- **Claude Code** (con modalità agentica abilitata) – [guida all’installazione](https://docs.anthropic.com/claude-code)
- **Python 3.9+** (per lo script scanner, opzionale)
- **Node.js** (per testare esempi JavaScript, opzionale)
- Terminale Unix (macOS/Linux)

## Installazione

```bash
git clone https://github.com/tuo-username/MigraAPI
cd MigraAPI
# Nessuna dipendenza esterna – tutto è bash/python standard
```

## Come usare MigraAPI

### Demo automatica con script orchestratore

```bash
./demo-script.sh
```

Esegue scanning simulato e produce un report `migration_report.json`.

### Utilizzo reale con Claude Code

1. Avvia Claude Code:
   ```bash
   claude
   ```
2. Chiedi la migrazione:
   ```
   Migra il codice in examples/before dalla vecchia API alla nuova usando la skill api-migration
   ```
Claude attiverà la skill, invocherà i subagent in parallelo e restituirà il risultato.

## Distribuzione come plugin

Puoi trasformare MigraAPI in un plugin distribuibile per Claude Code:

1. **Prepara la struttura** (già conforme):
   ```
   .claude/skills/api-migration/
   .claude/agents/
   ```

2. **Aggiungi il repository a un marketplace** (esempio con marketplace ufficiale):
   ```bash
   /plugin marketplace add anthropics/skills
   ```

3. **Installa il plugin** (una volta che lo hai pubblicato):
   ```bash
   /plugin install migrapi@your-org/skills
   ```

Per creare un marketplace personale, consulta la [documentazione ufficiale Anthropic](https://docs.anthropic.com/claude-code/plugins).

## Enterprise Managed Settings

In contesti aziendali, le Skills possono essere distribuite centralmente a tutti i membri del team:

- **Managed settings** permettono di preinstallare skill su tutte le workstation.
- Un amministratore può definire una policy che forza l’uso della skill `api-migration` in determinati repository.
- Le skill vengono aggiornate automaticamente quando il repository centrale cambia.

Questo approccio garantisce coerenza e riduce il carico di formazione.

## Best practice di sicurezza

- **Verifica sempre le skill da fonti esterne**: Prima di installare una skill da un repository non ufficiale, ispeziona il contenuto (soprattutto script eseguiti).
- **Usa `allowed-tools`** per limitare l’accesso a strumenti sensibili (es. `Write`, `Bash`). In questa skill, lo scanner ha solo strumenti di lettura.
- **Non includere secret o chiavi API** nei file della skill.
- **Esegui script in sandbox** quando possibile (es. container o ambienti isolati).
- **Audita le modifiche**: Per migrazioni critiche, usa il subagent `validator` per verificare ogni modifica prima di applicarla.

## Esempi

Prima della migrazione (`examples/before/sample.py`):
```python
from old_api import Client
client = Client(api_key="test")
user = client.get_user(user_id=123)
```

Dopo la migrazione (`examples/after/sample.py` – atteso):
```python
from new_api import Client
client = Client(api_key="test")
user = client.fetch_user_by_id(user_id=123)
```

Puoi eseguire il test automatico per verificare le regole:
```bash
python tests/test_migration.py
```

## Troubleshooting

### La skill non si attiva

**Sintomo**: Claude non usa la skill anche se il task è pertinente.

**Soluzioni**:
- Controlla il frontmatter di `SKILL.md`: `name` e `description` devono essere chiari e corrispondere al task.
- Verifica che la cartella della skill sia posizionata in `.claude/skills/api-migration/`.
- Prova a richiamare esplicitamente la skill: “Usa la skill api-migration per...”

### Lo scanner non trova occorrenze

**Sintomo**: `scanner.py` restituisce `"files": []`.

**Soluzioni**:
- Aggiorna i pattern in `regex-patterns.md` e `scanner.py` (sezione `PATTERNS`).
- Assicurati che i file da analizzare abbiano estensione `.py`, `.js`, `.mjs`, `.cjs`.
- Testa manualmente: `python .claude/skills/api-migration/scripts/scanner.py <file>`

### Errori di scrittura del rewriter

**Sintomo**: Il subagent `rewriter` restituisce `"status": "error"`.

**Soluzioni**:
- Verifica che i permessi del file consentano la scrittura.
- Controlla che `allowed-tools` nel subagent includa `Write` e `Edit`.
- Se il mapping causa sostituzioni parziali, modifica le regole in `migration-rules.json` (usa stringhe più specifiche).

### Validazione fallisce

**Sintomo**: `validator` restituisce errori di sintassi o test.

**Soluzioni**:
- Controlla l’output JSON: `errors` contiene riga e messaggio.
- Correggi manualmente il file o affina le regole di migrazione.
- Aggiungi un passo di validazione intermedia nel flusso di orchestrazione.

### Conflitti con altre skill o configurazioni

**Sintomo**: Comportamento inatteso, la skill non viene chiamata o interferisce con altre.

**Soluzioni**:
- Dai priorità esplicita: “Usa solo la skill api-migration”.
- Rimuovi temporaneamente altre skill dalla cartella `.claude/skills/`.
- In ambiente enterprise, verifica le impostazioni gestite.

### Debug generale

- **Monitora i log**: Claude Code produce output dettagliato con `--verbose`.
- **Chiedi auto-riflessione**: “Cosa è andato storto nella migrazione? Spiega i passi che hai seguito.”
- **Itera**: Migliora la skill basandoti sul feedback delle esecuzioni reali.

## Roadmap e contributi

- [ ] Integrazione completa con Claude Code (non solo simulazione).
- [ ] Supporto per più linguaggi (Java, Go, TypeScript).
- [ ] Plugin pubblicato su marketplace Anthropic.

Contributi sono benvenuti: fork e pull request.

## Licenza

MIT
