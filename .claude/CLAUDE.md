# MigraAPI – Project Configuration

This file provides global context for Claude Code when working on this repository.

## Project Overview
- **Purpose**: Demonstrates Claude Agent Skills + Subagents for API migration
- **Language**: Python 3.9+, JavaScript (Node 18+)
- **Key Skill**: `api-migration` – migrates deprecated API calls

## Default Behavior
- Always use the `api-migration` skill when the user mentions API migration or upgrade
- Output: structured JSON for subagent responses
- Never modify files outside `examples/` or `tests/` without explicit user confirmation

## File Structure
- `.claude/skills/api-migration/` – core Skill with rules and scanner
- `.claude/agents/` – scanner, rewriter, validator subagents
- `examples/before/` – code to migrate
- `examples/after/` – expected migration result

## Code Style
- Python: PEP 8 (enforced via ruff)
- Markdown: wrap at 80 characters
- JSON/YAML: 2 spaces indentation

## Testing
- Run: `python tests/test_migration.py` or `make test`

## Security
- Never commit API keys or secrets
- Scanner scripts run with read-only permissions
- Rewriter only modifies files in targeted directories
