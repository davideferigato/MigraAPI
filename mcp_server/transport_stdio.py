"""
STDIO transport configuration for MCP server.

This is the default transport for local execution with Claude Code/Desktop.
The server communicates via standard input/output streams using JSON-RPC.

To use:
    python -m mcp_server.server --transport stdio

Then configure Claude Desktop with:
{
    "mcpServers": {
        "migrapi": {
            "command": "python",
            "args": ["-m", "mcp_server.server", "--transport", "stdio"],
            "cwd": "/path/to/MigraAPI"
        }
    }
}
"""

# The STDIO transport is handled by the mcp.run(transport="stdio") call in server.py
# This file serves as documentation for the configuration.
