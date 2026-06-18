"""
Core migration logic for MCP server.

Reuses the existing scanner, rewriter, and validator implementations.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import existing implementations
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from .scanner_adapter import scan_file as _scan_file, scan_directory as _scan_directory
from .rewriter_adapter import rewrite_file as _rewrite_file
from .validator_adapter import validate_file as _validate_file


def load_migration_rules() -> Dict[str, Any]:
    """Load migration rules from the skill's JSON file."""
    rules_path = PROJECT_ROOT / ".claude" / "skills" / "api-migration" / "migration-rules.json"
    try:
        with open(rules_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Migration rules not found", "rules": []}


def scan_file(file_path: str) -> Dict[str, Any]:
    """Scan a single file for deprecated API calls."""
    return _scan_file(file_path)


def scan_directory(directory_path: str) -> Dict[str, Any]:
    """Recursively scan a directory for deprecated API calls."""
    return _scan_directory(directory_path)


def rewrite_file(file_path: str, dry_run: bool = False) -> Dict[str, Any]:
    """Apply migration changes to a file."""
    return _rewrite_file(file_path, dry_run=dry_run)


def validate_file(file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
    """Validate a migrated file for syntax correctness."""
    return _validate_file(file_path, language)
