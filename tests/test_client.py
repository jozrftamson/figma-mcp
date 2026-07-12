"""
Tests for Figma MCP Server
"""

import pytest
from unittest.mock import AsyncMock, patch
from figma_mcp.client import FigmaClient


@pytest.mark.asyncio
async def test_figma_client_initialization():
    """Test FigmaClient initialization."""
    client = FigmaClient("test_token_12345")
    assert client.api_token == "test_token_12345"
    assert "X-Figma-Token" in client.headers


@pytest.mark.asyncio
async def test_list_teams():
    """Test list_teams method."""
    client = FigmaClient("test_token")
    
    with patch.object(client, '_request') as mock_request:
        mock_request.return_value = {
            "teams": [
                {"id": "1", "name": "Team A", "role": "owner"},
                {"id": "2", "name": "Team B", "role": "member"}
            ]
        }
        
        result = await client.list_teams()
        assert "result" in result
        assert len(result["result"]) == 2
        assert result["result"][0]["name"] == "Team A"


@pytest.mark.asyncio
async def test_get_file():
    """Test get_file method."""
    client = FigmaClient("test_token")
    
    with patch.object(client, '_request') as mock_request:
        mock_request.return_value = {
            "name": "Test File",
            "key": "abc123",
            "version": "1",
            "document": {"children": [{"id": "1"}]},
            "lastModified": "2024-01-01T00:00:00Z"
        }
        
        result = await client.get_file("abc123")
        assert "result" in result
        assert result["result"]["name"] == "Test File"
