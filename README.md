# Figma MCP Server

Model Context Protocol integration for the Figma API. Brings Figma files, components, and design tokens into any MCP-compatible AI application.

## Features

- **File Operations**: Get file structure, list files, export files
- **Component Management**: List components, get component details, search components
- **Tokens & Variables**: Access design tokens and variables
- **Team & Project Tools**: List teams, projects, and collaborate
- **Design System Access**: Retrieve design system information
- **Real-time Capabilities**: Watch file changes, get version history

## Installation

### From PyPI

```bash
pip install figma-mcp
```

### From Source

```bash
git clone https://github.com/yourusername/figma-mcp.git
cd figma-mcp
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

### 1. Get Your Figma API Token

- Go to [Figma Settings → Account](https://www.figma.com/settings)
- Create a personal access token
- Save it securely

### 2. Configure for Hermes

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  figma:
    command: "python"
    args: ["-m", "figma_mcp"]
    env:
      FIGMA_API_TOKEN: "${FIGMA_API_TOKEN}"
    timeout: 120
    connect_timeout: 30
```

### 3. Set Environment Variable

Create `~/.hermes/.env`:

```bash
FIGMA_API_TOKEN=your_personal_access_token_here
```

### 4. Register with Hermes

```bash
hermes mcp add figma --command python --args -m figma_mcp
hermes mcp test figma
hermes mcp list
```

## Available Tools

### Files

- **get_file** - Retrieve full file structure and metadata
- **get_file_nodes** - Get specific nodes from a file
- **list_files** - List files in a team
- **get_file_versions** - Get version history of a file
- **export_node** - Export node as PNG/SVG/PDF

### Components

- **list_components** - List all components in a file
- **get_component** - Get component details
- **search_components** - Search components by name
- **get_component_sets** - Get component sets/variants

### Variables & Tokens

- **list_variables** - List design variables
- **get_variable** - Get variable details
- **list_local_variables** - List variables in a file

### Team & Projects

- **list_teams** - List accessible teams
- **list_projects** - List projects in a team
- **list_team_components** - List components across team

### Design Systems

- **get_design_system** - Retrieve design system info
- **list_design_system_files** - List design system files

## Usage Examples

### With Hermes CLI

```bash
# List all Figma files in your workspace
hermes ask "What Figma files do I have? Use the figma tools."

# Get component details
hermes ask "Show me all button components from my design system using get_component_sets"

# Export a design
hermes ask "Export the 'HomeScreen' node from file abc123xyz as PNG"
```

### Programmatic Use

```python
from figma_mcp import FigmaClient

client = FigmaClient(api_token="your_token")

# Get file
file_data = await client.get_file("file_id")
print(file_data["name"])

# List components
components = await client.list_components("file_id")
for comp in components:
    print(f"Component: {comp['name']}")
```

## API Reference

### Authentication

All requests require a valid `FIGMA_API_TOKEN` environment variable.

### Tool Inputs

Each tool accepts a JSON object with parameters. Example:

```json
{
  "file_key": "abc123xyz",
  "ids": ["1:2", "3:4"]
}
```

### Tool Outputs

All tools return JSON with:

```json
{
  "result": "success data",
  "error": null
}
```

Or on error:

```json
{
  "result": null,
  "error": "Error message"
}
```

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Type Checking

```bash
mypy figma_mcp/
```

### Format Code

```bash
black figma_mcp/
isort figma_mcp/
```

### Lint

```bash
ruff check figma_mcp/
```

## Architecture

```
figma_mcp/
├── server.py          # MCP Server entry point
├── client.py          # Figma API client
├── tools/
│   ├── files.py       # File operations
│   ├── components.py  # Component tools
│   ├── variables.py   # Variables & tokens
│   ├── teams.py       # Team tools
│   └── design_systems.py
├── models.py          # Pydantic models
├── errors.py          # Custom exceptions
└── utils.py           # Utilities
```

## Troubleshooting

### "MCP server is not connected"

```bash
hermes mcp test figma
```

Check the error output. Most common issues:

1. **Invalid token**: Verify `FIGMA_API_TOKEN` is set correctly
2. **Network error**: Ensure you can reach `api.figma.com`
3. **Version mismatch**: Update MCP SDK: `pip install --upgrade mcp`

### "Tool call timed out"

Increase timeout in config:

```yaml
mcp_servers:
  figma:
    timeout: 300
    connect_timeout: 60
```

### "Permission denied"

Your token may lack scopes. Regenerate with all permissions enabled.

## Limitations

- Personal access tokens can't access private/shared files outside your workspace
- Some endpoints require specific team/project permissions
- Real-time subscriptions not currently supported (batch polling instead)

## Roadmap

- [ ] Real-time file change subscriptions
- [ ] Webhook support for file updates
- [ ] Batch operations
- [ ] File upload/creation
- [ ] Prototype and interaction data
- [ ] Constraint and interaction details
- [ ] Plugin API integration

## Contributing

Contributions are encouraged! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-tool`)
3. Add tests for your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Related Resources

- [Figma API Docs](https://www.figma.com/developers/api)
- [MCP Specification](https://modelcontextprotocol.io)
- [Hermes Integration Guide](https://github.com/NousResearch/hermes-agent)
- [Docker MCP Catalog](https://hub.docker.com/u/mcp)

## Support

- 📖 [Documentation](https://github.com/yourusername/figma-mcp#readme)
- 🐛 [Issues](https://github.com/yourusername/figma-mcp/issues)
- 💬 [Discussions](https://github.com/yourusername/figma-mcp/discussions)
