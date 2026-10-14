"""
Figma MCP Package
"""

__version__ = "0.1.0"
__author__ = "Figma MCP Contributors"

from figma_mcp.client import FigmaClient


def __getattr__(name: str):
    if name == "server":
        from figma_mcp.server import server

        return server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["FigmaClient", "server"]
