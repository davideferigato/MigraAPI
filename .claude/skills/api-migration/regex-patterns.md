# Regex patterns for detecting deprecated API calls

Used by `scanner.py`. Syntax: Python `re` module.

## Python patterns

| Pattern | Description |
|---------|-------------|
| `old_api\.get_user\s*\(` | Matches `old_api.get_user(` |
| `old_api\.fetch_posts\s*\(` | Matches `old_api.fetch_posts(` |
| `from\s+old_api\s+import` | Matches import statements |

## JavaScript patterns

| Pattern | Description |
|---------|-------------|
| `oldApi\.getUser\s*\(` | Matches `oldApi.getUser(` |
| `oldApi\.fetchPosts\s*\(` | Matches `oldApi.fetchPosts(` |
| `require\s*\(\s*['"]old-api['"]\s*\)` | Matches `require('old-api')` |

## Adding new patterns

Extend the pattern dictionary in `scanner.py` accordingly.
