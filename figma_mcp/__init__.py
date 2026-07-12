"""
Figma MCP Package
"""

__version__ = "0.1.0"
__author__ = "Figma MCP Contributors"

from figma_mcp.client import FigmaClient
from figma_mcp.server import server

__all__ = ["FigmaClient", "server"]
