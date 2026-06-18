"""
Orchestrator for the full migration pipeline: scan → rewrite → validate.
"""

from pathlib import Path
from typing import Any, Dict, List

from .core import scan_directory, rewrite_file, validate_file


def run_migration_pipeline(
    source_directory: str,
    dry_run: bool = False,
    max_files: int = 100
) -> Dict[str, Any]:
    """
    Run the full migration pipeline on a directory.

    Args:
        source_directory: Directory containing code to migrate.
        dry_run: If True, preview changes without writing.
        max_files: Maximum number of files to process.

    Returns:
        JSON with summary of all operations.
    """
    path = Path(source_directory)
    if not path.exists():
        return {
            "status": "error",
            "directory": str(path),
            "error": f"Directory not found: {source_directory}"
        }

    # Step 1: Scan
    scan_result = scan_directory(str(path))
    if scan_result.get("status") == "error":
        return scan_result

    files = scan_result.get("files", [])
    if not files:
        return {
            "status": "success",
            "directory": str(path),
            "files_scanned": 0,
            "files_modified": 0,
            "changes_made": 0,
            "message": "No deprecated API calls found"
        }

    # Limit files if needed
    if len(files) > max_files:
        files = files[:max_files]

    # Step 2: Rewrite each file
    rewrite_results = []
    for file_info in files:
        file_path = file_info.get("path")
        if not file_path:
            continue
        result = rewrite_file(file_path, dry_run=dry_run)
        rewrite_results.append(result)

    # Step 3: Validate each modified file
    validation_results = []
    for result in rewrite_results:
        if result.get("status") == "success" and result.get("changes_made", 0) > 0:
            file_path = result.get("file")
            if file_path:
                validation_results.append(validate_file(file_path))

    # Compile summary
    total_changes = sum(r.get("changes_made", 0) for r in rewrite_results)
    files_modified = sum(1 for r in rewrite_results if r.get("changes_made", 0) > 0)
    errors = [r for r in validation_results if r.get("status") == "error"]

    return {
        "status": "success" if not errors else "partial",
        "directory": str(path),
        "dry_run": dry_run,
        "files_scanned": len(files),
        "files_modified": files_modified,
        "changes_made": total_changes,
        "errors": errors,
        "details": {
            "rewrite_results": rewrite_results,
            "validation_results": validation_results
        }
    }
