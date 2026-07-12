"""FastAPI web server for Figma MCP Server - Railway deployment."""

import os
import asyncio
import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import MCP server components
try:
    from figma_mcp.server import TOOLS
    from figma_mcp.client import FigmaClient
except ImportError:
    # Fallback if imports fail
    TOOLS = {}
    FigmaClient = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Figma MCP Server",
    description="Model Context Protocol server for Figma API",
    version="1.0.0",
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Figma client
figma_token = os.getenv("FIGMA_API_TOKEN")
figma_client = FigmaClient(figma_token) if FigmaClient and figma_token else None


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - service status."""
    return {
        "status": "healthy",
        "service": "Figma MCP Server",
        "version": "1.0.0",
        "tools_available": len(TOOLS),
        "authenticated": figma_client is not None,
    }


@app.get("/health")
async def health():
    """Railway health check endpoint."""
    return {
        "status": "ok",
        "service": "figma-mcp",
        "uptime": "running",
    }


@app.get("/status")
async def status():
    """Detailed status information."""
    return {
        "service": "Figma MCP Server",
        "status": "operational",
        "version": "1.0.0",
        "tools": len(TOOLS),
        "authenticated": figma_client is not None,
        "port": os.getenv("PORT", "8000"),
        "environment": os.getenv("ENVIRONMENT", "production"),
    }


# ============================================================================
# Tools Endpoints
# ============================================================================

@app.get("/tools")
async def list_tools():
    """List all available MCP tools."""
    return {
        "tools": list(TOOLS.keys()),
        "count": len(TOOLS),
        "categories": {
            "file": [t for t in TOOLS.keys() if "file" in t.lower()],
            "component": [t for t in TOOLS.keys() if "component" in t.lower()],
            "variable": [t for t in TOOLS.keys() if "variable" in t.lower()],
            "team": [t for t in TOOLS.keys() if "team" in t.lower()],
            "project": [t for t in TOOLS.keys() if "project" in t.lower()],
        }
    }


@app.get("/tools/{tool_name}")
async def get_tool_info(tool_name: str):
    """Get information about a specific tool."""
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    return {
        "name": tool_name,
        "available": True,
        "description": TOOLS[tool_name].__doc__ or "No description",
    }


# ============================================================================
# Figma API Endpoints
# ============================================================================

@app.get("/api/teams")
async def get_teams():
    """Get all teams from Figma."""
    if not figma_client:
        raise HTTPException(status_code=401, detail="Not authenticated with Figma API")
    
    try:
        teams = await figma_client.list_teams()
        return {
            "status": "success",
            "teams": teams,
            "count": len(teams) if isinstance(teams, list) else 0,
        }
    except Exception as e:
        logger.error(f"Error fetching teams: {e}")
        return {
            "status": "error",
            "error": str(e),
            "details": "Failed to fetch teams from Figma API",
        }


@app.get("/api/projects/{team_id}")
async def get_projects(team_id: str):
    """Get projects for a team."""
    if not figma_client:
        raise HTTPException(status_code=401, detail="Not authenticated with Figma API")
    
    try:
        projects = await figma_client.list_projects(team_id)
        return {
            "status": "success",
            "team_id": team_id,
            "projects": projects,
            "count": len(projects) if isinstance(projects, list) else 0,
        }
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return {
            "status": "error",
            "error": str(e),
            "team_id": team_id,
        }


@app.get("/api/file/{file_key}")
async def get_file(file_key: str):
    """Get file details from Figma."""
    if not figma_client:
        raise HTTPException(status_code=401, detail="Not authenticated with Figma API")
    
    try:
        file_data = await figma_client.get_file(file_key)
        return {
            "status": "success",
            "file": file_data,
        }
    except Exception as e:
        logger.error(f"Error fetching file {file_key}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "file_key": file_key,
        }


@app.get("/api/components/{file_key}")
async def get_components(file_key: str):
    """Get components from a Figma file."""
    if not figma_client:
        raise HTTPException(status_code=401, detail="Not authenticated with Figma API")
    
    try:
        components = await figma_client.list_components(file_key)
        return {
            "status": "success",
            "file_key": file_key,
            "components": components,
            "count": len(components) if isinstance(components, list) else 0,
        }
    except Exception as e:
        logger.error(f"Error fetching components: {e}")
        return {
            "status": "error",
            "error": str(e),
            "file_key": file_key,
        }


@app.get("/api/variables/{file_key}")
async def get_variables(file_key: str):
    """Get variables from a Figma file."""
    if not figma_client:
        raise HTTPException(status_code=401, detail="Not authenticated with Figma API")
    
    try:
        variables = await figma_client.list_variables(file_key)
        return {
            "status": "success",
            "file_key": file_key,
            "variables": variables,
            "count": len(variables) if isinstance(variables, list) else 0,
        }
    except Exception as e:
        logger.error(f"Error fetching variables: {e}")
        return {
            "status": "error",
            "error": str(e),
            "file_key": file_key,
        }


# ============================================================================
# Tool Execution Endpoint
# ============================================================================

@app.post("/api/call")
async def call_tool(tool_name: str, **kwargs):
    """Call a tool with parameters."""
    if tool_name not in TOOLS:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{tool_name}' not found. Available: {list(TOOLS.keys())}"
        )
    
    try:
        tool_func = TOOLS[tool_name]
        
        # Call function (async or sync)
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(**kwargs)
        else:
            result = tool_func(**kwargs)
        
        return {
            "status": "success",
            "tool": tool_name,
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error calling tool {tool_name}: {e}")
        return {
            "status": "error",
            "tool": tool_name,
            "error": str(e),
        }


# ============================================================================
# Documentation Endpoints
# ============================================================================

@app.get("/docs-tools")
async def tools_documentation():
    """Documentation for all available tools."""
    docs = {}
    for tool_name, tool_func in TOOLS.items():
        docs[tool_name] = {
            "description": tool_func.__doc__ or "No description",
            "name": tool_name,
        }
    
    return {
        "tools": docs,
        "total": len(TOOLS),
        "endpoint": "/api/call",
        "usage": "POST /api/call?tool_name=TOOL&param1=value1&param2=value2",
    }


@app.get("/api-reference")
async def api_reference():
    """Complete API reference."""
    return {
        "service": "Figma MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "status": {
                "GET /": "Root status",
                "GET /health": "Health check (for Railway)",
                "GET /status": "Detailed status",
            },
            "tools": {
                "GET /tools": "List all tools",
                "GET /tools/{tool_name}": "Get tool info",
                "POST /api/call": "Execute a tool",
            },
            "figma_api": {
                "GET /api/teams": "List teams",
                "GET /api/projects/{team_id}": "List projects",
                "GET /api/file/{file_key}": "Get file info",
                "GET /api/components/{file_key}": "List components",
                "GET /api/variables/{file_key}": "List variables",
            },
            "documentation": {
                "GET /docs-tools": "Tool documentation",
                "GET /api-reference": "This reference",
            },
        },
        "authentication": "Requires FIGMA_API_TOKEN environment variable",
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": "Not found",
            "path": str(request.url.path),
            "available_endpoints": {
                "root": "/",
                "health": "/health",
                "tools": "/tools",
                "api_reference": "/api-reference",
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "details": str(exc),
        },
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "production")
    
    logger.info(f"Starting Figma MCP Server on port {port}")
    logger.info(f"Environment: {environment}")
    logger.info(f"Tools available: {len(TOOLS)}")
    logger.info(f"Authenticated: {figma_client is not None}")
    
    uvicorn.run(
        "figma_mcp.web_server:app",
        host="0.0.0.0",
        port=port,
        reload=(environment == "development"),
        log_level="info",
    )
