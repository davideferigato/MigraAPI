"""
Adapter for the validator logic to work with MCP server.
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def validate_file(file_path: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate a migrated file for syntax correctness.

    Args:
        file_path: Path to the file to validate.
        language: Optional language hint ('python' or 'javascript').

    Returns:
        JSON with status, validity, and errors.
    """
    path = Path(file_path)
    if not path.exists():
        return {
            "status": "error",
            "file": str(path),
            "error": f"File not found: {file_path}"
        }

    # Detect language from extension if not provided
    if language is None:
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

    errors = []

    if language == "python":
        try:
            # Python syntax check
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                # Parse error output
                for line in result.stderr.splitlines():
                    if "SyntaxError" in line or "IndentationError" in line:
                        errors.append({
                            "type": "syntax",
                            "message": line.strip()
                        })
        except subprocess.TimeoutExpired:
            errors.append({"type": "timeout", "message": "Validation timed out"})

    elif language == "javascript":
        # JavaScript syntax check via node
        try:
            result = subprocess.run(
                ["node", "--check", str(path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                for line in result.stderr.splitlines():
                    if "SyntaxError" in line:
                        errors.append({
                            "type": "syntax",
                            "message": line.strip()
                        })
        except FileNotFoundError:
            # Node not installed
            errors.append({
                "type": "warning",
                "message": "Node.js not found, skipping JavaScript validation"
            })
        except subprocess.TimeoutExpired:
            errors.append({"type": "timeout", "message": "Validation timed out"})

    if errors:
        return {
            "status": "error",
            "file": str(path),
            "valid": False,
            "errors": errors,
            "suggestion": "Check syntax and migration mapping for the affected lines"
        }

    return {
        "status": "success",
        "file": str(path),
        "valid": True,
        "checks_passed": ["syntax"],
        "message": "File is valid"
    }
