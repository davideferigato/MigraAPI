"""
Streamable HTTP transport configuration for MCP server.

Allows the MCP server to be deployed as a remote microservice,
accessible from any MCP client over HTTP.

To run:
    python -m mcp_server.server --transport streamable-http --port 8000

Then configure Claude Desktop with:
{
    "mcpServers": {
        "migrapi-remote": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http"
        }
    }
}

For production deployment:
    1. Deploy to a cloud service (AWS, GCP, Azure, etc.)
    2. Use a reverse proxy (nginx, Caddy) for TLS termination
    3. Add authentication middleware if needed

The Streamable HTTP transport is the current standard for remote MCP deployments
(protocol version 2025-03-26).[reference:20]
"""

# The Streamable HTTP transport is handled by the mcp.run(transport="streamable-http")
# call in server.py. This file serves as documentation.
