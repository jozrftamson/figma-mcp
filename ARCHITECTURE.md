# 🏗️ Figma MCP Server - Technical Architecture & Extension Guide

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Hermes Agent                     │
│              (or any MCP client)                    │
└────────────────────┬────────────────────────────────┘
                     │
                     │ MCP Protocol
                     │ (stdio/HTTP)
                     │
┌────────────────────▼────────────────────────────────┐
│         Figma MCP Server (Main Process)             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │         MCP Server Implementation           │  │
│  │  (handles tool discovery & routing)         │  │
│  └────────────────┬────────────────────────────┘  │
│                   │                                │
│  ┌────────────────▼────────────────────────────┐  │
│  │         Tool Registry & Router              │  │
│  │  (routes calls to specific handlers)        │  │
│  └────────────────┬────────────────────────────┘  │
│                   │                                │
│  ┌────────────────▼────────────────────────────┐  │
│  │    Handler Layer (Tool Implementations)     │  │
│  │                                             │  │
│  │  ┌─────────────┐  ┌──────────────┐        │  │
│  │  │File Handler │  │Component     │  ...   │  │
│  │  │Operations   │  │Handler       │        │  │
│  │  └─────────────┘  └──────────────┘        │  │
│  └────────────────┬────────────────────────────┘  │
│                   │                                │
│  ┌────────────────▼────────────────────────────┐  │
│  │      Figma API Client Layer                 │  │
│  │  (HTTP client + request handling)           │  │
│  └────────────────┬────────────────────────────┘  │
│                   │                                │
└───────────────────┼────────────────────────────────┘
                    │
                    │ HTTPS
                    │
        ┌───────────▼──────────┐
        │   Figma API v1       │
        │   api.figma.com      │
        └──────────────────────┘
```

---

## Code Organization

```
figma_mcp/
├── server.py              # MCP server main entry point
│                         # - Initializes server
│                         # - Registers tools
│                         # - Routes requests
│
├── client.py              # Figma API client
│                         # - HTTP requests
│                         # - Response parsing
│                         # - Error handling
│
├── tools/
│   ├── __init__.py        # Tool registry
│   ├── files.py          # File operations
│   ├── components.py     # Component tools
│   ├── variables.py      # Variable tools
│   └── teams.py          # Team tools
│
├── models.py              # Pydantic models
│                         # - Request/response types
│                         # - Validation schemas
│
├── errors.py              # Custom exceptions
│
└── utils.py               # Utilities
                           # - Helpers, formatting
```

---

## Extension Points

### 1. Adding a New Tool

```python
# File: figma_mcp/tools/new_feature.py

async def new_tool(param1: str, param2: int = None) -> dict:
    """New tool description.
    
    Args:
        param1: Parameter description
        param2: Optional parameter
        
    Returns:
        Result dictionary
    """
    try:
        # 1. Validate inputs
        if not param1:
            raise ValueError("param1 required")
        
        # 2. Call Figma API
        endpoint = f"/endpoint/{param1}"
        data = await figma_client._request("GET", endpoint)
        
        # 3. Transform & return
        return {"result": data}
    except Exception as e:
        return {"error": str(e)}

# Register in server.py
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "new_tool":
        return await new_tool(arguments.get("param1"))
```

### 2. Adding a New API Endpoint

```python
# File: figma_mcp/client.py

async def new_endpoint(self, arg: str) -> dict:
    """Access new Figma API endpoint."""
    endpoint = f"/files/{arg}/new-endpoint"
    try:
        data = await self._request("GET", endpoint)
        return {"result": data}
    except httpx.HTTPError as e:
        logger.error(f"API error: {e}")
        raise
```

### 3. Adding a New Model

```python
# File: figma_mcp/models.py

from pydantic import BaseModel, Field

class NewFeatureResponse(BaseModel):
    """Response model for new feature."""
    
    id: str = Field(..., description="Feature ID")
    name: str = Field(..., description="Feature name")
    metadata: dict = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc123",
                "name": "Example",
                "metadata": {}
            }
        }
```

---

## Enhancement Patterns

### Pattern 1: Caching Layer

```python
# Add to client.py

from functools import lru_cache
import time

class CachedFigmaClient(FigmaClient):
    def __init__(self, api_token: str, cache_ttl: int = 300):
        super().__init__(api_token)
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_times = {}
    
    async def _request_cached(self, method: str, endpoint: str, **kwargs):
        """Request with caching."""
        cache_key = f"{method}:{endpoint}"
        
        # Check cache
        if cache_key in self._cache:
            if time.time() - self._cache_times[cache_key] < self.cache_ttl:
                return self._cache[cache_key]
        
        # Fetch & cache
        data = await self._request(method, endpoint, **kwargs)
        self._cache[cache_key] = data
        self._cache_times[cache_key] = time.time()
        return data
```

### Pattern 2: Batch Operations

```python
# Add to client.py

async def batch_get_files(self, file_keys: List[str]) -> List[dict]:
    """Get multiple files efficiently."""
    tasks = [
        self.get_file(key) 
        for key in file_keys
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

### Pattern 3: Webhook Handler

```python
# New file: figma_mcp/webhooks.py

from fastapi import FastAPI, HTTPException
from typing import Callable

class WebhookManager:
    def __init__(self):
        self.handlers = {}
    
    def register(self, event_type: str, handler: Callable):
        """Register webhook handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def handle_webhook(self, event_type: str, data: dict):
        """Process webhook event."""
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                await handler(data)
```

### Pattern 4: Rate Limiting

```python
# Add to client.py

from ratelimit import limits, sleep_and_retry
import time

class RateLimitedFigmaClient(FigmaClient):
    # Figma API: ~120 requests per minute
    @sleep_and_retry
    @limits(calls=120, period=60)
    async def _request(self, method: str, endpoint: str, **kwargs):
        """Rate-limited request."""
        return await super()._request(method, endpoint, **kwargs)
```

---

## Testing New Features

### Unit Test Template

```python
# File: tests/test_new_feature.py

import pytest
from unittest.mock import AsyncMock, patch
from figma_mcp.client import FigmaClient

@pytest.mark.asyncio
async def test_new_tool():
    """Test new tool functionality."""
    client = FigmaClient("test_token")
    
    with patch.object(client, '_request') as mock_request:
        mock_request.return_value = {"result": "test_data"}
        
        result = await client.new_tool("param1")
        
        assert "result" in result
        mock_request.assert_called_once()
```

### Integration Test Template

```python
# File: tests/test_integration_new_feature.py

@pytest.mark.asyncio
async def test_new_tool_integration():
    """Test with real Figma API (requires valid token)."""
    import os
    token = os.getenv("FIGMA_API_TOKEN")
    if not token:
        pytest.skip("FIGMA_API_TOKEN not set")
    
    client = FigmaClient(token)
    
    # Use test file from environment or skip
    test_file_key = os.getenv("TEST_FILE_KEY")
    if not test_file_key:
        pytest.skip("TEST_FILE_KEY not set")
    
    result = await client.new_tool(test_file_key)
    assert "result" in result or "error" in result
```

---

## Performance Optimization Guide

### 1. Async Best Practices

```python
# GOOD: Parallel requests
tasks = [client.get_file(key) for key in file_keys]
results = await asyncio.gather(*tasks)

# BAD: Sequential requests
results = [await client.get_file(key) for key in file_keys]
```

### 2. Connection Pooling

```python
# Reuse HTTP client
async with httpx.AsyncClient() as client:
    await client.get(url1)
    await client.get(url2)  # Reuses connection
```

### 3. Pagination Handling

```python
async def get_all_components_paginated(self, file_key: str):
    """Handle paginated results."""
    all_components = []
    cursor = None
    
    while True:
        result = await self.get_components(file_key, cursor=cursor)
        all_components.extend(result.get("components", []))
        
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    
    return all_components
```

---

## Debugging & Logging

### Enhanced Logging

```python
# Add to client.py

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# In methods:
logger.debug(f"Calling API endpoint: {endpoint}")
logger.info(f"Successfully retrieved file: {file_key}")
logger.warning(f"API rate limit approaching: {remaining_calls}")
logger.error(f"API error occurred: {error}")
```

### Request/Response Logging

```python
async def _request_with_logging(self, method: str, endpoint: str, **kwargs):
    """Request with detailed logging."""
    logger.debug(f"→ {method} {endpoint}")
    logger.debug(f"  Headers: {self.headers}")
    
    try:
        response = await self._request(method, endpoint, **kwargs)
        logger.debug(f"← {method} {endpoint}: 200")
        logger.debug(f"  Response size: {len(str(response))} bytes")
        return response
    except Exception as e:
        logger.error(f"✗ {method} {endpoint}: {e}")
        raise
```

---

## Building a Plugin System

```python
# File: figma_mcp/plugins.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class FigmaMCPPlugin(ABC):
    """Base class for plugins."""
    
    name: str
    version: str
    description: str
    
    @abstractmethod
    async def initialize(self, client):
        """Called on startup."""
        pass
    
    @abstractmethod
    async def on_tool_call(self, tool_name: str, args: Dict) -> Any:
        """Called before each tool execution."""
        pass
    
    @abstractmethod
    async def on_tool_result(self, tool_name: str, result: Any) -> Any:
        """Called after each tool execution."""
        pass

# Example plugin
class LoggingPlugin(FigmaMCPPlugin):
    name = "logging_plugin"
    version = "1.0.0"
    description = "Enhanced logging"
    
    async def initialize(self, client):
        logger.info(f"Loaded plugin: {self.name}")
    
    async def on_tool_call(self, tool_name: str, args: Dict):
        logger.info(f"Calling tool: {tool_name} with args: {args}")
    
    async def on_tool_result(self, tool_name: str, result: Any):
        logger.info(f"Tool result: {tool_name} → {result}")
```

---

## Deployment Considerations

### Docker Deployment

```dockerfile
# Dockerfile for containerized MCP server
FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .

ENV FIGMA_API_TOKEN=""
ENV MCP_LOG_LEVEL="INFO"

EXPOSE 8080
CMD ["python", "-m", "figma_mcp.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: figma-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: figma-mcp-server
  template:
    metadata:
      labels:
        app: figma-mcp-server
    spec:
      containers:
      - name: figma-mcp
        image: figma-mcp:latest
        env:
        - name: FIGMA_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: figma-credentials
              key: api-token
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
```

---

## Contributing Extensions

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/my-extension`
3. **Implement following patterns above**
4. **Add comprehensive tests**
5. **Update ROADMAP.md**
6. **Submit PR with description**

---

This architecture is designed to be extensible. Each layer can be enhanced independently while maintaining backward compatibility.

