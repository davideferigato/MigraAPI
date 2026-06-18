"""
Adapter for the existing scanner.py to work with MCP server.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
SCANNER_SCRIPT = PROJECT_ROOT / ".claude" / "skills" / "api-migration" / "scripts" / "scanner.py"


def scan_file(file_path: str) -> Dict[str, Any]:
    """
    Scan a single file using the existing scanner.py.

    Returns:
        JSON with status, file, and occurrences.
    """
    path = Path(file_path)
    if not path.exists():
        return {
            "status": "error",
            "file": str(path),
            "error": f"File not found: {file_path}"
        }

    try:
        result = subprocess.run(
            [sys.executable, str(SCANNER_SCRIPT), str(path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return {
                "status": "error",
                "file": str(path),
                "error": result.stderr or "Scanner failed"
            }

        data = json.loads(result.stdout)
        files = data.get("files", [])
        if files:
            return {
                "status": "success",
                "file": str(path),
                "occurrences": files[0].get("occurrences", [])
            }
        else:
            return {
                "status": "success",
                "file": str(path),
                "occurrences": []
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "file": str(path),
            "error": "Scanner timed out"
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "file": str(path),
            "error": f"Invalid JSON from scanner: {e}"
        }


def scan_directory(directory_path: str) -> Dict[str, Any]:
    """
    Recursively scan a directory using the existing scanner.py.

    Returns:
        JSON with status and list of files with occurrences.
    """
    path = Path(directory_path)
    if not path.exists():
        return {
            "status": "error",
            "directory": str(path),
            "error": f"Directory not found: {directory_path}"
        }

    try:
        result = subprocess.run(
            [sys.executable, str(SCANNER_SCRIPT), str(path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            return {
                "status": "error",
                "directory": str(path),
                "error": result.stderr or "Scanner failed"
            }

        data = json.loads(result.stdout)
        return {
            "status": "success",
            "directory": str(path),
            "files": data.get("files", [])
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "directory": str(path),
            "error": "Scanner timed out"
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "directory": str(path),
            "error": f"Invalid JSON from scanner: {e}"
        }
