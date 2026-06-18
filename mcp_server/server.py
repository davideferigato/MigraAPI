#!/usr/bin/env python3
"""
MigraAPI MCP Server - Core server implementation.

Exposes tools, resources, and prompts for API migration via MCP.
Uses FastMCP for minimal boilerplate.

Run with STDIO:
    python -m mcp_server.server

Run with Streamable HTTP:
    python -m mcp_server.server --transport streamable-http --port 8000
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# Import core migration logic
from .core import (
    scan_file,
    rewrite_file,
    validate_file,
    load_migration_rules,
    scan_directory,
)

# Initialize FastMCP server
mcp = FastMCP("MigraAPI", json_response=True)

# ============================================================
# TOOLS
# ============================================================

@mcp.tool()
def scan_file_tool(file_path: str) -> Dict[str, Any]:
    """
    Scan a single file for deprecated API calls.

    Args:
        file_path: Path to the file to scan (absolute or relative to project root).

    Returns:
        JSON with status, file path, and list of occurrences.
    """
    return scan_file(file_path)


@mcp.tool()
def scan_directory_tool(directory_path: str) -> Dict[str, Any]:
    """
    Recursively scan a directory for deprecated API calls in all supported files.

    Args:
        directory_path: Path to the directory to scan.

    Returns:
        JSON with status and list of files with occurrences.
    """
    return scan_directory(directory_path)


@mcp.tool()
def rewrite_file_tool(
    file_path: str,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Apply migration changes to a file based on migration rules.

    Args:
        file_path: Path to the file to rewrite.
        dry_run: If True, preview changes without writing.

    Returns:
        JSON with status, changes made, and details.
    """
    return rewrite_file(file_path, dry_run=dry_run)


@mcp.tool()
def validate_file_tool(
    file_path: str,
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate a migrated file for syntax correctness.

    Args:
        file_path: Path to the file to validate.
        language: Optional language hint ('python' or 'javascript').

    Returns:
        JSON with status, validity, and errors if any.
    """
    return validate_file(file_path, language)


@mcp.tool()
def migrate_codebase_tool(
    source_directory: str,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Full migration pipeline: scan → rewrite → validate all files in a directory.

    Args:
        source_directory: Directory containing code to migrate.
        dry_run: If True, preview changes without writing.

    Returns:
        JSON with summary of all operations.
    """
    from .orchestrator import run_migration_pipeline
    return run_migration_pipeline(source_directory, dry_run=dry_run)


# ============================================================
# RESOURCES
# ============================================================

@mcp.resource("migration-rules://current")
def get_migration_rules() -> str:
    """
    Get the current migration rules as a JSON string.

    This resource provides the complete mapping from deprecated API calls
    to new API calls for both Python and JavaScript.
    """
    rules = load_migration_rules()
    return json.dumps(rules, indent=2)


@mcp.resource("migration-rules://language/{language}")
def get_migration_rules_for_language(language: str) -> str:
    """
    Get migration rules filtered by language.

    Args:
        language: 'python' or 'javascript'

    Returns:
        JSON string with rules for the specified language.
    """
    rules = load_migration_rules()
    filtered = [r for r in rules.get("rules", []) if r.get("language") == language]
    return json.dumps({"language": language, "rules": filtered}, indent=2)


# ============================================================
# PROMPTS
# ============================================================

@mcp.prompt()
def migrate_codebase_prompt(
    source_directory: str,
    target_directory: Optional[str] = None
) -> str:
    """
    Generate a prompt for migrating a codebase from deprecated to new API.

    Args:
        source_directory: Directory containing code to migrate.
        target_directory: Optional directory to write migrated files (default: same).

    Returns:
        A structured prompt for Claude to execute the migration.
    """
    rules = load_migration_rules()
    rules_summary = "\n".join([
        f"  - {r['old']} → {r['new']} ({r.get('language', 'unknown')})"
        for r in rules.get("rules", [])[:10]
    ])
    if len(rules.get("rules", [])) > 10:
        rules_summary += f"\n  ... and {len(rules['rules']) - 10} more rules"

    return f"""
# Migrate Codebase from Deprecated API to New API

## Source Directory
{source_directory}

## Target Directory
{target_directory or source_directory}

## Migration Rules
{rules_summary}

## Instructions
1. Use the `scan_directory_tool` to find all deprecated API calls.
2. For each file with occurrences, use `rewrite_file_tool` to apply changes.
3. After rewriting, use `validate_file_tool` to verify syntax.
4. Provide a summary report of all changes made.

## Output Format
Return a structured JSON report with:
- files_scanned: int
- files_modified: int
- changes_made: int
- errors: list of errors (if any)
- status: "success" | "partial" | "error"
"""


@mcp.prompt()
def resolve_ambiguity_prompt(
    old_pattern: str,
    context: str = ""
) -> str:
    """
    Generate a prompt to resolve ambiguous migration rules.

    Args:
        old_pattern: The deprecated API pattern that is ambiguous.
        context: Additional context about the code.

    Returns:
        A prompt asking Claude to help resolve the ambiguity.
    """
    return f"""
# Resolve Migration Ambiguity

## Deprecated Pattern
`{old_pattern}`

## Context
{context or "No additional context provided."}

## Question
How should this pattern be migrated? There may be multiple possible new API mappings.

## Instructions
1. Analyze the pattern and context.
2. Suggest the most appropriate new API mapping.
3. Explain your reasoning.

## Output Format
Return JSON with:
- suggested_mapping: str (the new API call)
- confidence: float (0.0 to 1.0)
- reasoning: str
- alternative_mappings: list of alternatives
"""


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="MigraAPI MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for HTTP transport (default: 127.0.0.1)"
    )
    args = parser.parse_args()

    if args.transport == "streamable-http":
        print(f"🚀 Starting MigraAPI MCP Server on http://{args.host}:{args.port}/mcp", file=sys.stderr)
        mcp.run(
            transport="streamable-http",
            host=args.host,
            port=args.port,
            path="/mcp"
        )
    else:
        # STDIO transport - do NOT print to stdout (would corrupt JSON-RPC)[reference:14]
        print("🚀 Starting MigraAPI MCP Server (STDIO transport)", file=sys.stderr)
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
