# 🤝 Contributing to Figma MCP Server

Danke, dass du zum Figma MCP Server beitragen möchtest! Dieses Dokument beschreibt, wie du mithelfen kannst.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

Bitte lies und befolge unseren [Code of Conduct](CODE_OF_CONDUCT.md).

Kurz gefasst:
- 🤝 Sei respektvoll und inklusiv
- 🚫 Keine Diskriminierung oder Belästigung
- 💬 Konstruktives Feedback geben
- 🎯 Fokus auf das Projekt, nicht auf Personen

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Besuche https://github.com/jozrftamson/figma-mcp
# Klicke auf "Fork" Button oben rechts
```

### 2. Clone your Fork

```bash
git clone https://github.com/YOUR_USERNAME/figma-mcp.git
cd figma-mcp
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/jozrftamson/figma-mcp.git
git remote -v
# origin    https://github.com/YOUR_USERNAME/figma-mcp.git
# upstream  https://github.com/jozrftamson/figma-mcp.git
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- Git
- pip

### Setup Development Environment

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install with dev dependencies
pip install -e ".[dev]"

# 3. Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Verify Setup

```bash
# Run tests
pytest tests/ -v

# Type checking
mypy figma_mcp/

# Linting
ruff check figma_mcp/

# Formatting
black --check figma_mcp/
```

## 🔧 Making Changes

### 1. Create Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout upstream/master

# Create feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

```
feature/add-export-tool          # Neue Funktionalität
bugfix/fix-token-parsing         # Bug Fix
docs/update-readme               # Dokumentation
refactor/optimize-client         # Refactoring
test/add-component-tests         # Tests
```

### 2. Make your Changes

Bearbeite die Dateien im Editor deiner Wahl.

**Wichtig:**
- Schreibe Tests für neue Features
- Update Dokumentation
- Follow Coding Standards (siehe unten)
- Ein Commit = Ein logischer Change

### 3. Keep Branch Updated

```bash
# Hol Updates vom Upstream
git fetch upstream
git rebase upstream/master

# Falls Merge Konflikte: Editiere Dateien und
git add .
git rebase --continue
```

## 📤 Submitting Changes

### 1. Push to your Fork

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

- Besuche https://github.com/jozrftamson/figma-mcp
- Klicke "New Pull Request"
- Wähle dein Fork und Feature Branch
- Beschreibe deine Changes

### PR Title Format

```
[TYPE] Brief description of changes

Types: feat, fix, docs, refactor, test, chore
Examples:
  feat: Add export_node tool for PNG/SVG export
  fix: Handle missing file_key in get_file
  docs: Update Hermes configuration guide
```

### PR Description Template

```markdown
## Description
Kurze Beschreibung was geändert wurde.

## Related Issues
Fixes #123
Related to #456

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Unit tests added/updated
- [ ] Tested locally
- [ ] No regressions

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No new warnings generated
```

## 💻 Coding Standards

### Python Style Guide

Wir folgen [PEP 8](https://pep8.org/) mit Tools:

```bash
# Format code
black figma_mcp/

# Sort imports
isort figma_mcp/

# Lint
ruff check figma_mcp/

# Type check
mypy figma_mcp/
```

### Type Hints

```python
# ✅ GOOD
async def get_file(self, file_key: str, version: str | None = None) -> dict:
    """Get file structure and metadata.
    
    Args:
        file_key: Figma file key
        version: Optional version ID
        
    Returns:
        Dictionary with file data
    """
    pass

# ❌ BAD
async def get_file(self, file_key, version=None):
    pass
```

### Docstrings

```python
# ✅ GOOD - Google Style
def list_components(self, file_key: str) -> dict:
    """List all components in a Figma file.
    
    Fetches component list from the Figma API and returns
    formatted data with name, key, and metadata.
    
    Args:
        file_key: The Figma file key from URL
        
    Returns:
        Dictionary with 'result' key containing component list
        
    Raises:
        httpx.HTTPError: If API request fails
        ValueError: If file_key is invalid
        
    Example:
        >>> client = FigmaClient(api_token)
        >>> result = await client.list_components("abc123")
        >>> print(result["result"])
    """
    pass
```

### Comments

```python
# ✅ GOOD - Explains WHY, not WHAT
async def _wait_for_session(self, timeout: float) -> bool:
    # Retry with exponential backoff to handle transient network issues
    # while respecting the user's configured timeout
    backoff = 1.0
    while time.time() < deadline:
        backoff = min(backoff * 2, 60.0)
        
# ❌ BAD - Obvious from code
backoff = 1.0  # Set backoff to 1.0
```

### Error Handling

```python
# ✅ GOOD - Specific errors
try:
    response = await client.get_file(file_key)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        logger.error("Authentication failed: %s", e)
        raise ValueError("Invalid API token") from e
    raise

# ❌ BAD - Catch everything
try:
    response = await client.get_file(file_key)
except Exception:
    pass
```

### Logging

```python
# ✅ GOOD - Structured logging
logger.info("MCP server '%s' connected with %d tools", server_name, tool_count)
logger.warning("Tool call timeout after %ds for server '%s'", timeout, server_name)
logger.error("Failed to list components: %s", error, exc_info=True)

# ❌ BAD - String interpolation
logger.info(f"Server {server_name} connected")
```

## 🧪 Testing

### Writing Tests

```python
# tests/test_new_feature.py
import pytest
from unittest.mock import AsyncMock, patch
from figma_mcp.client import FigmaClient


@pytest.mark.asyncio
async def test_export_node_png():
    """Test exporting a node as PNG."""
    client = FigmaClient("test_token")
    
    with patch.object(client, '_request') as mock_request:
        mock_request.return_value = {
            "images": {"1:2": "https://example.com/node.png"}
        }
        
        result = await client.export_node("file123", "1:2", "PNG")
        
        assert "images" in result
        assert result["images"]["1:2"].endswith(".png")
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_client.py -v

# Specific test
pytest tests/test_client.py::test_get_file -v

# With coverage
pytest tests/ --cov=figma_mcp --cov-report=html
```

### Test Coverage

Ziel: **80%+ Coverage**

```bash
# Check coverage
pytest tests/ --cov=figma_mcp

# Generate HTML report
pytest tests/ --cov=figma_mcp --cov-report=html
# Öffne htmlcov/index.html im Browser
```

## 📚 Documentation

### Updating README

- Halte Features aktuell
- Update Installation Instructions
- Add Beispiele für neue Tools
- Fix Typos und Links

### Adding Comments

- Erkläre WARUM, nicht WAS
- Update Docstrings wenn API ändert
- Add Links zu relevanten Issues

### Writing Docs

```markdown
# Feature Title

Brief description.

## Usage

Code example showing how to use the feature.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| name | str | Description |

## Returns

Description of return value.

## Example

```python
result = await client.new_method()
```
```

## 🎯 Development Workflow Summary

```bash
# 1. Setup
git clone https://github.com/YOUR_USERNAME/figma-mcp.git
cd figma-mcp
git remote add upstream https://github.com/jozrftamson/figma-mcp.git

# 2. Create feature
git checkout -b feature/my-feature

# 3. Make changes & test
# ... edit files ...
pytest tests/ -v
black figma_mcp/
mypy figma_mcp/

# 4. Commit
git add .
git commit -m "feat: Add my feature"

# 5. Keep updated
git fetch upstream
git rebase upstream/master

# 6. Push
git push origin feature/my-feature

# 7. Create PR on GitHub
# → https://github.com/jozrftamson/figma-mcp/pulls
```

## 🚀 Ideas for Contributions

### New Features

- [ ] Real-time file subscriptions
- [ ] Webhook support for file updates
- [ ] Batch operations
- [ ] File upload/creation
- [ ] Prototype and interaction data
- [ ] Design token export
- [ ] Component variant handling
- [ ] Version diff tool

### Bug Fixes

- [ ] Error message improvements
- [ ] Timeout handling
- [ ] Edge case handling
- [ ] Performance optimization

### Documentation

- [ ] Tutorial videos
- [ ] Architecture documentation
- [ ] API reference
- [ ] Troubleshooting guide
- [ ] Migration guide

### Testing

- [ ] Increase test coverage
- [ ] Add integration tests
- [ ] Add stress tests
- [ ] Add edge case tests

### Tools

- [ ] GitHub Actions CI/CD
- [ ] Pre-commit hooks
- [ ] Docker setup
- [ ] Dev container

## 📞 Getting Help

### Questions?

- Check [README.md](README.md)
- Look at [Issues](https://github.com/jozrftamson/figma-mcp/issues)
- Open [Discussion](https://github.com/jozrftamson/figma-mcp/discussions)

### Found a Bug?

```bash
# Check if already reported
# https://github.com/jozrftamson/figma-mcp/issues

# Create new issue with:
# - Description of bug
# - Steps to reproduce
# - Expected vs actual behavior
# - Environment (Python version, OS, etc.)
```

## ✨ Recognition

Contributors werden anerkannt in:
- README.md Contributors Sektion
- Release Notes
- GitHub Contributors Graph

## 📋 Checklist Before Submitting PR

- [ ] Fork erstellt und Feature Branch
- [ ] Upstream Remote hinzugefügt
- [ ] Code auf Style geprüft (`black`, `ruff`)
- [ ] Type hints überall (`mypy`)
- [ ] Tests geschrieben/updated
- [ ] Tests grün (`pytest`)
- [ ] Dokumentation updated
- [ ] Commits sauber und aussagekräftig
- [ ] PR Description vollständig
- [ ] Branch aktuell mit upstream

## 🎉 Thank You!

Danke für deine Unterstützung des Figma MCP Server Projekts!

---

**Happy Contributing!** 🚀
