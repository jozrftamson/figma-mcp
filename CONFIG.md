# Figma MCP Server Configuration

This directory contains all tools and integration points for Figma MCP server.

## Quick Start

```bash
# Install
pip install -e .

# Test
figma-mcp

# With Hermes
hermes mcp add figma --command python --args -m figma_mcp
```

## Directory Structure

```
.
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── pyproject.toml              # Project configuration
├── .gitignore                  # Git ignore patterns
├── figma_mcp/
│   ├── __init__.py             # Package initialization
│   ├── server.py               # MCP server main entry
│   ├── client.py               # Figma API client
│   └── tools/
│       └── __init__.py         # Tool definitions
└── tests/
    ├── conftest.py             # Pytest configuration
    └── test_client.py          # Client tests
```

## Environment Variables

Required:
- `FIGMA_API_TOKEN` - Your Figma personal access token

Optional:
- `FIGMA_API_TIMEOUT` - Request timeout in seconds (default: 30)
- `LOG_LEVEL` - Logging level (default: INFO)

## Available Tools

See README.md for complete tool documentation.
