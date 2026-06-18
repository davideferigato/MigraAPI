"""
Adapter for the rewriter logic to work with MCP server.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / ".claude" / "skills" / "api-migration" / "migration-rules.json"


def load_rules() -> List[Dict[str, Any]]:
    """Load migration rules from the skill's JSON file."""
    try:
        with open(RULES_FILE, "r") as f:
            data = json.load(f)
            return data.get("rules", [])
    except FileNotFoundError:
        return []


def rewrite_file(file_path: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    Apply migration changes to a file.

    Args:
        file_path: Path to the file to rewrite.
        dry_run: If True, preview changes without writing.

    Returns:
        JSON with status and changes made.
    """
    path = Path(file_path)
    if not path.exists():
        return {
            "status": "error",
            "file": str(path),
            "error": f"File not found: {file_path}"
        }

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {
            "status": "error",
            "file": str(path),
            "error": f"Failed to read file: {e}"
        }

    # Determine language from extension
    ext = path.suffix.lower()
    if ext in [".py"]:
        language = "python"
    elif ext in [".js", ".mjs", ".cjs"]:
        language = "javascript"
    else:
        return {
            "status": "error",
            "file": str(path),
            "error": f"Unsupported file extension: {ext}"
        }

    rules = load_rules()
    lang_rules = [r for r in rules if r.get("language") == language]
    # Sort by length descending to avoid partial replacements
    lang_rules.sort(key=lambda x: -len(x.get("old", "")))

    changes = []
    new_content = content

    for rule in lang_rules:
        old = rule.get("old", "")
        new = rule.get("new", "")
        if not old or not new:
            continue

        # Count occurrences before replacement
        pattern = re.escape(old)
        count_before = len(re.findall(pattern, new_content))

        # Replace all occurrences
        new_content = re.sub(pattern, new, new_content)

        count_after = len(re.findall(pattern, new_content))
        replaced = count_before - count_after

        if replaced > 0:
            changes.append({
                "old": old,
                "new": new,
                "replaced": replaced
            })

    if not dry_run:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
        except Exception as e:
            return {
                "status": "error",
                "file": str(path),
                "error": f"Failed to write file: {e}"
            }

    return {
        "status": "success",
        "file": str(path),
        "dry_run": dry_run,
        "changes_made": len(changes),
        "changes": changes
    }
