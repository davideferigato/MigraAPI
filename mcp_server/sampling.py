"""
Sampling implementation for MCP server (Advanced Topics).

Allows the server to request LLM completions from the client
to resolve ambiguities in migration rules.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP


def register_sampling_handlers(mcp: FastMCP) -> None:
    """
    Register sampling-related handlers with the MCP server.

    Sampling allows the server to ask the client (Claude) for help
    resolving ambiguous migration patterns.
    """

    @mcp.sampling()
    async def resolve_migration_ambiguity(
        old_pattern: str,
        context: str = "",
        alternatives: List[str] = None
    ) -> Dict[str, Any]:
        """
        Request sampling from the client to resolve migration ambiguity.

        Args:
            old_pattern: The deprecated API pattern that is ambiguous.
            context: Additional context about the code.
            alternatives: List of possible new API mappings.

        Returns:
            Suggested migration mapping from the LLM.
        """
        # This is a placeholder - the actual sampling is handled by the MCP client.
        # The client (Claude) will provide the completion.
        return {
            "old_pattern": old_pattern,
            "context": context,
            "alternatives": alternatives or [],
            "suggested_mapping": None,  # Will be filled by client
            "confidence": 0.0,
            "reasoning": "Awaiting sampling response from client"
        }
