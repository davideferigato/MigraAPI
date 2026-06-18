"""
Progress notifications for MCP server (Advanced Topics).

Provides real-time progress updates during long-running operations
like scanning large directories.
"""

import asyncio
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP


class ProgressTracker:
    """Track and emit progress notifications for long operations."""

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp
        self.total = 0
        self.current = 0
        self.message = ""

    def start(self, total: int, message: str = "Starting operation") -> None:
        """Start a new progress tracking session."""
        self.total = total
        self.current = 0
        self.message = message
        self._emit_progress()

    def update(self, increment: int = 1, message: Optional[str] = None) -> None:
        """Update progress by increment."""
        self.current += increment
        if message:
            self.message = message
        self._emit_progress()

    def _emit_progress(self) -> None:
        """Emit a progress notification via MCP."""
        # The MCP SDK handles progress notifications automatically
        # when using the context parameter in tools.
        # This is a placeholder for the pattern.
        pass


def register_progress_handlers(mcp: FastMCP) -> None:
    """
    Register progress-related handlers with the MCP server.

    This demonstrates the pattern for progress notifications.
    In practice, the MCP SDK's context parameter provides
    progress reporting capabilities.
    """

    @mcp.tool()
    async def scan_with_progress(directory_path: str) -> Dict[str, Any]:
        """
        Scan a directory with progress notifications.

        This demonstrates how to use progress notifications
        during a long-running operation.
        """
        from pathlib import Path
        import sys

        path = Path(directory_path)
        if not path.exists():
            return {"status": "error", "error": f"Directory not found: {directory_path}"}

        # Find all Python and JavaScript files
        files = []
        for ext in [".py", ".js", ".mjs", ".cjs"]:
            files.extend(list(path.rglob(f"*{ext}")))

        total = len(files)
        if total == 0:
            return {"status": "success", "files_scanned": 0, "message": "No files found"}

        results = []
        # In a real implementation with MCP context, you would emit progress
        # notifications here. The pattern would be:
        #
        # for i, file in enumerate(files):
        #     await context.report_progress(i + 1, total, f"Scanning {file.name}")
        #     results.append(scan_file(str(file)))

        # Simulated progress for demonstration
        for i, file in enumerate(files):
            # Simulate work
            await asyncio.sleep(0.01)
            # In a real implementation, use context.report_progress()
            results.append({
                "file": str(file),
                "status": "scanned",
                "progress": f"{i + 1}/{total}"
            })

        return {
            "status": "success",
            "files_scanned": total,
            "files": results
        }
