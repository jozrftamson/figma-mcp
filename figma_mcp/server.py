"""
Figma MCP Server - Main entry point
"""

import asyncio
import json
import logging
import os
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

from figma_mcp.client import FigmaClient
from figma_mcp.tools import (
    register_file_tools,
    register_component_tools,
    register_variable_tools,
    register_team_tools,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP Server
server = Server("figma-mcp")

# Global Figma client
figma_client: FigmaClient | None = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Figma tools."""
    tools = []
    
    # File Tools
    tools.extend([
        Tool(
            name="get_file",
            description="Retrieve complete file structure and metadata from Figma",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_key": {
                        "type": "string",
                        "description": "Figma file key (found in URL: /file/{FILE_KEY}/...)"
                    },
                    "version": {
                        "type": "string",
                        "description": "Optional version ID to get specific version"
                    }
                },
                "required": ["file_key"]
            }
        ),
        Tool(
            name="get_file_nodes",
            description="Get specific nodes from a Figma file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_key": {"type": "string", "description": "Figma file key"},
                    "ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Node IDs to retrieve (comma-separated or array)"
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Depth of nested content to retrieve (default: 1)"
                    }
                },
                "required": ["file_key", "ids"]
            }
        ),
        Tool(
            name="list_files",
            description="List all files accessible in a team",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "string",
                        "description": "Team ID to list files from"
                    }
                },
                "required": ["team_id"]
            }
        ),
        Tool(
            name="get_file_versions",
            description="Get version history of a Figma file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_key": {"type": "string", "description": "Figma file key"}
                },
                "required": ["file_key"]
            }
        ),
    ])
    
    # Component Tools
    tools.extend([
        Tool(
            name="list_components",
            description="List all components in a Figma file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_key": {"type": "string", "description": "Figma file key"}
                },
                "required": ["file_key"]
            }
        ),
        Tool(
            name="get_component",
            description="Get detailed information about a specific component",
            inputSchema={
                "type": "object",
                "properties": {
                    "component_key": {
                        "type": "string",
                        "description": "Component key (found in list_components)"
                    }
                },
                "required": ["component_key"]
            }
        ),
        Tool(
            name="search_components",
            description="Search for components by name across a team",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {"type": "string", "description": "Team ID"},
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["team_id", "query"]
            }
        ),
    ])
    
    # Variable Tools
    tools.extend([
        Tool(
            name="list_variables",
            description="List all variables in a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_key": {"type": "string", "description": "Figma file key"}
                },
                "required": ["file_key"]
            }
        ),
        Tool(
            name="get_variable",
            description="Get details about a specific variable",
            inputSchema={
                "type": "object",
                "properties": {
                    "variable_id": {
                        "type": "string",
                        "description": "Variable ID"
                    }
                },
                "required": ["variable_id"]
            }
        ),
    ])
    
    # Team Tools
    tools.extend([
        Tool(
            name="list_teams",
            description="List all accessible teams",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_projects",
            description="List projects in a team",
            inputSchema={
                "type": "object",
                "properties": {
                    "team_id": {"type": "string", "description": "Team ID"}
                },
                "required": ["team_id"]
            }
        ),
    ])
    
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    """Execute a Figma tool."""
    if figma_client is None:
        return TextContent(text=json.dumps({
            "error": "Figma client not initialized. Set FIGMA_API_TOKEN environment variable."
        }))
    
    try:
        result = await route_tool_call(name, arguments)
        return TextContent(text=json.dumps(result))
    except Exception as e:
        logger.error(f"Tool execution failed: {name}", exc_info=True)
        return TextContent(text=json.dumps({
            "error": str(e),
            "tool": name
        }))


async def route_tool_call(name: str, arguments: dict) -> dict:
    """Route tool calls to appropriate handlers."""
    
    # File tools
    if name == "get_file":
        return await figma_client.get_file(
            arguments.get("file_key"),
            version=arguments.get("version")
        )
    elif name == "get_file_nodes":
        return await figma_client.get_file_nodes(
            arguments.get("file_key"),
            arguments.get("ids"),
            depth=arguments.get("depth", 1)
        )
    elif name == "list_files":
        return await figma_client.list_files(arguments.get("team_id"))
    elif name == "get_file_versions":
        return await figma_client.get_file_versions(arguments.get("file_key"))
    
    # Component tools
    elif name == "list_components":
        return await figma_client.list_components(arguments.get("file_key"))
    elif name == "get_component":
        return await figma_client.get_component(arguments.get("component_key"))
    elif name == "search_components":
        return await figma_client.search_components(
            arguments.get("team_id"),
            arguments.get("query")
        )
    
    # Variable tools
    elif name == "list_variables":
        return await figma_client.list_variables(arguments.get("file_key"))
    elif name == "get_variable":
        return await figma_client.get_variable(arguments.get("variable_id"))
    
    # Team tools
    elif name == "list_teams":
        return await figma_client.list_teams()
    elif name == "list_projects":
        return await figma_client.list_projects(arguments.get("team_id"))
    
    else:
        return {"error": f"Unknown tool: {name}"}


async def main():
    """Main entry point for MCP server."""
    global figma_client
    
    api_token = os.getenv("FIGMA_API_TOKEN")
    if not api_token:
        logger.error("FIGMA_API_TOKEN environment variable not set")
        return
    
    figma_client = FigmaClient(api_token)
    logger.info("Figma MCP Server starting...")
    
    async with server:
        logger.info("Figma MCP Server ready and listening")
        await asyncio.Event().wait()


def run():
    """Entry point for console script."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
