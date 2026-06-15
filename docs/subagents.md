# Designing Effective Subagents

Subagents are isolated assistants with their own context window. They are invoked via the `Task` tool in Claude Code.

## Structure of a subagent file

Each subagent is a `.md` file inside `.claude/agents/` with YAML frontmatter and a prompt.

Example: `scanner.md`

```yaml
---
name: scanner
description: Scans a single source file for deprecated API calls.
tools: Read, Grep, Glob
prompt: |
  You are a scanner subagent...
```

## Key principles

### 1. Structured output
Always return JSON with a clear schema. Include `status` (success/error), the file path, and relevant data.

```json
{
  "status": "success",
  "file": "path/to/file",
  "occurrences": [...]
}
```

### 2. Obstacle reporting
If anything fails (missing file, permission denied), return an error status with details.

```json
{
  "status": "error",
  "file": "path/to/file",
  "error": "File not found"
}
```

### 3. Limit tools
Only give the subagent the tools it needs. Scanner does not need `Write`. Rewriter does not need `Bash`.

### 4. Avoid inter-subagent dependencies
Subagents never communicate directly. The orchestrator collects results and passes them as input to the next subagent.

## Example: rewriter subagent

```yaml
---
name: rewriter
tools: Read, Write, Edit
prompt: |
  Apply migration mapping to a file. Return JSON with changes_made.
```

## Best practices

- Keep prompts concise but precise.
- Specify output format exactly (no extra text).
- Test subagents with simple inputs before integrating.

For the full implementation, see `.claude/agents/` in the repository.
