---
name: api-migration
description: Migrates deprecated API calls to a new API version in Python and JavaScript codebases. Use this skill when the user asks to migrate code from an old API to a new API, upgrade API endpoints, or replace deprecated function calls.
allowed-tools: Read, Grep, Glob, Bash(scripts/scanner.py)
---

# API Migration Skill

This skill enables Claude to automatically migrate code from a deprecated API to a new API. It works with Python and JavaScript/Node.js projects.

## How to use this skill

1. **Understand the migration scope** – ask the user for old/new API names or use default mapping from `migration-rules.json`.
2. **Scan the codebase** – run `python scripts/scanner.py <path>` to get a JSON report of deprecated calls.
3. **Apply migrations** (via subagents) – replace old calls with new ones, preserving formatting and comments.
4. **Validate** – run tests or linters; report obstacles.

## Files

- `migration-rules.json` – core mapping old → new.
- `regex-patterns.md` – regex patterns for detection.
- `scripts/scanner.py` – executable scanner that outputs JSON.

## Example migration

**Before (Python):**
```python
from old_api import Client
client = Client(api_key="test")
user = client.get_user(user_id=123)
```

**After:**
```python
from new_api import Client
client = Client(api_key="test")
user = client.fetch_user_by_id(user_id=123)
```

## Allowed tools

Only read tools plus `scanner.py` execution. Writing is delegated to subagents with explicit `write` permissions.

## Troubleshooting

- Skill not activating? Check `name`/`description` match user request.
- Scanner fails? Ensure Python 3.9+ and `re` module (built-in).
- No occurrences? Verify regex patterns against actual code.
