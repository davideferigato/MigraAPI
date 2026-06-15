# Architecture of MigraAPI

MigraAPI follows the **orchestrator pattern** where a main agent (Claude Code) delegates tasks to isolated subagents. The system leverages **progressive disclosure** to manage context efficiently.

## Overall flow

```mermaid
graph TD
    U[User request] --> O[Orchestrator Claude Code]
    O --> S[Skill: api-migration]
    S --> |loads rules| R[migration-rules.json]
    O --> |Task| SC[Subagent: scanner]
    O --> |Task| RW[Subagent: rewriter]
    O --> |Task| V[Subagent: validator]
    SC --> |JSON| O
    RW --> |JSON| O
    V --> |JSON| O
    O --> |report| U
```

## Progressive Disclosure (3 levels)

```mermaid
flowchart LR
    subgraph Level1[Level 1: Discovery]
        A[Claude starts] --> B[Load only name+description]
    end
    subgraph Level2[Level 2: Activation]
        C[Task matches skill] --> D[Load full SKILL.md]
    end
    subgraph Level3[Level 3: Execution]
        E[Need extra files/scripts] --> F[Load rules.json, run scanner.py]
    end
    Level1 --> Level2 --> Level3
```

## Subagent isolation

Each subagent runs in its own context window. The main agent never sees the full source code of scanned files – only the structured JSON output. This keeps the main context small and allows parallel execution.

## Parallel execution

The orchestrator can launch multiple `scanner` subagents in parallel (one per file). Results are aggregated. Similarly, `rewriter` and `validator` can run in parallel on independent files.

## Allowed tools

- **scanner**: `Read`, `Grep`, `Glob` (read-only)
- **rewriter**: `Read`, `Write`, `Edit` (modify files)
- **validator**: `Read`, `Bash`, `Grep` (run syntax checks)

This follows the principle of least privilege.

For more details, see the [Subagents page](subagents.md).
