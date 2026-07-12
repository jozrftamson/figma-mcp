"""
Figma API Client
"""

import httpx
import logging
from typing import Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FigmaClient:
    """Figma API client for MCP integration."""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, api_token: str):
        """Initialize Figma client with API token."""
        self.api_token = api_token
        self.headers = {
            "X-Figma-Token": api_token,
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to Figma API."""
        url = f"{self.BASE_URL}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    headers=self.headers,
                    timeout=30.0,
                    **kwargs
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Figma API error: {e}")
                raise
    
    # File Operations
    
    async def get_file(self, file_key: str, version: Optional[str] = None) -> dict:
        """Get file structure and metadata."""
        try:
            endpoint = f"/files/{file_key}"
            if version:
                endpoint += f"?version={version}"
            data = await self._request("GET", endpoint)
            return {
                "result": {
                    "name": data.get("name"),
                    "key": data.get("key"),
                    "version": data.get("version"),
                    "pages": len(data.get("document", {}).get("children", [])),
                    "modified_at": data.get("lastModified"),
                    "created_at": data.get("createdAt"),
                    "documents": data.get("document")
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_file_nodes(
        self, 
        file_key: str, 
        ids: list | str,
        depth: int = 1
    ) -> dict:
        """Get specific nodes from file."""
        try:
            if isinstance(ids, str):
                ids = ids.split(",")
            ids_param = ",".join(ids)
            endpoint = f"/files/{file_key}/nodes?ids={ids_param}&depth={depth}"
            data = await self._request("GET", endpoint)
            return {"result": data.get("nodes", {})}
        except Exception as e:
            return {"error": str(e)}
    
    async def list_files(self, team_id: str) -> dict:
        """List files in a team."""
        try:
            endpoint = f"/teams/{team_id}/files"
            data = await self._request("GET", endpoint)
            files = []
            for file in data.get("files", []):
                files.append({
                    "name": file.get("name"),
                    "key": file.get("key"),
                    "last_modified": file.get("last_modified"),
                    "thumbnail_url": file.get("thumbnail_url")
                })
            return {"result": files}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_file_versions(self, file_key: str) -> dict:
        """Get version history."""
        try:
            endpoint = f"/files/{file_key}/versions"
            data = await self._request("GET", endpoint)
            versions = []
            for version in data.get("versions", []):
                versions.append({
                    "id": version.get("id"),
                    "created_at": version.get("created_at"),
                    "label": version.get("label"),
                    "description": version.get("description"),
                    "user": version.get("user", {}).get("handle")
                })
            return {"result": versions}
        except Exception as e:
            return {"error": str(e)}
    
    # Component Operations
    
    async def list_components(self, file_key: str) -> dict:
        """List all components in a file."""
        try:
            endpoint = f"/files/{file_key}/components"
            data = await self._request("GET", endpoint)
            components = []
            for comp in data.get("components", []):
                components.append({
                    "key": comp.get("key"),
                    "name": comp.get("name"),
                    "description": comp.get("description"),
                    "created_at": comp.get("created_at"),
                    "updated_at": comp.get("updated_at")
                })
            return {"result": components}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_component(self, component_key: str) -> dict:
        """Get component details."""
        try:
            endpoint = f"/components/{component_key}"
            data = await self._request("GET", endpoint)
            return {
                "result": {
                    "key": data.get("key"),
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "documentation_links": data.get("documentationLinks", []),
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at")
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def search_components(self, team_id: str, query: str) -> dict:
        """Search components by name."""
        try:
            endpoint = f"/teams/{team_id}/components/search?q={query}"
            data = await self._request("GET", endpoint)
            results = []
            for comp in data.get("meta", []):
                results.append({
                    "key": comp.get("key"),
                    "name": comp.get("name"),
                    "file_key": comp.get("file_key"),
                    "description": comp.get("description")
                })
            return {"result": results}
        except Exception as e:
            return {"error": str(e)}
    
    # Variable Operations
    
    async def list_variables(self, file_key: str) -> dict:
        """List all variables in a file."""
        try:
            endpoint = f"/files/{file_key}/variables/local"
            data = await self._request("GET", endpoint)
            variables = []
            for var in data.get("variables", {}).values():
                variables.append({
                    "id": var.get("id"),
                    "name": var.get("name"),
                    "value": var.get("value"),
                    "type": var.get("type"),
                    "description": var.get("description")
                })
            return {"result": variables}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_variable(self, variable_id: str) -> dict:
        """Get variable details."""
        try:
            # Figma API doesn't have direct variable endpoint, 
            # return from file variables list
            return {
                "result": {
                    "id": variable_id,
                    "note": "Use list_variables with file_key to see variable details"
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    # Team Operations
    
    async def list_teams(self) -> dict:
        """List all accessible teams."""
        try:
            endpoint = "/me/teams"
            data = await self._request("GET", endpoint)
            teams = []
            for team in data.get("teams", []):
                teams.append({
                    "id": team.get("id"),
                    "name": team.get("name"),
                    "role": team.get("role")
                })
            return {"result": teams}
        except Exception as e:
            return {"error": str(e)}
    
    async def list_projects(self, team_id: str) -> dict:
        """List projects in a team."""
        try:
            endpoint = f"/teams/{team_id}/projects"
            data = await self._request("GET", endpoint)
            projects = []
            for proj in data.get("projects", []):
                projects.append({
                    "id": proj.get("id"),
                    "name": proj.get("name"),
                    "file_count": proj.get("file_count")
                })
            return {"result": projects}
        except Exception as e:
            return {"error": str(e)}
