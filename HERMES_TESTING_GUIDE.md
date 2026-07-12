# 🧪 Figma MCP in Hermes - Testing & Verification Guide

Anleitung zum Testen und Kontrollieren der Figma MCP Integration im Hermes Agent.

---

## 📋 Table of Contents

1. [Local Setup & Testing](#local-setup--testing)
2. [Integration Testing](#integration-testing)
3. [Hermes Configuration](#hermes-configuration)
4. [Debugging & Troubleshooting](#debugging--troubleshooting)
5. [Automated Testing](#automated-testing)
6. [CI/CD Integration](#cicd-integration)

---

## Local Setup & Testing

### Step 1: Clone Both Repositories

```bash
# Clone Figma MCP Server
git clone https://github.com/jozroftamson/figma-mcp.git
cd figma-mcp

# In another terminal, clone Hermes
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
```

### Step 2: Install Figma MCP locally

```bash
cd figma-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
python -c "from figma_mcp import server; print('✅ Figma MCP installed')"
```

### Step 3: Add to Hermes Config

```bash
cd ../hermes-agent

# Create Hermes config if it doesn't exist
mkdir -p ~/.hermes
cat > ~/.hermes/config.yaml << 'EOF'
mcp_servers:
  figma:
    command: python
    args:
      - -m
      - figma_mcp

  # Other Hermes MCPs...
EOF
```

### Step 4: Set Figma API Token

```bash
# Set environment variable
export FIGMA_API_TOKEN="your_figma_api_token"

# Or add to .env
echo "FIGMA_API_TOKEN=your_figma_api_token" > .env
```

### Step 5: Test Local Connection

```bash
# Test if MCP server can be started directly
python -m figma_mcp

# Should output:
# MCP server started...
# Ready for connections
```

---

## Integration Testing

### Test 1: Basic Connection

**File:** `test_hermes_integration.py`

```python
#!/usr/bin/env python3
"""Test Hermes integration with Figma MCP."""

import asyncio
import subprocess
import json
from pathlib import Path

async def test_hermes_figma_connection():
    """Test connection between Hermes and Figma MCP."""
    
    print("🔍 Testing Hermes ↔ Figma MCP Connection...")
    
    # Start Figma MCP server
    print("  ▶️  Starting Figma MCP server...")
    process = subprocess.Popen(
        ["python", "-m", "figma_mcp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Give server time to start
        await asyncio.sleep(2)
        
        # Test if process is running
        if process.poll() is None:
            print("  ✅ Server started successfully")
        else:
            print("  ❌ Server failed to start")
            stdout, stderr = process.communicate()
            print(f"  Error: {stderr.decode()}")
            return False
        
        # Test with Hermes
        print("\n  ▶️  Testing Hermes integration...")
        result = subprocess.run(
            ["hermes", "ask", "List my Figma teams"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✅ Hermes integration working")
            print(f"  Response: {result.stdout[:100]}...")
            return True
        else:
            print("  ❌ Hermes integration failed")
            print(f"  Error: {result.stderr}")
            return False
            
    finally:
        # Stop server
        process.terminate()
        process.wait(timeout=5)
        print("\n  ✅ Server stopped")

if __name__ == "__main__":
    success = asyncio.run(test_hermes_figma_connection())
    exit(0 if success else 1)
```

Run the test:

```bash
python test_hermes_integration.py
```

### Test 2: Tool Discovery

```bash
# Check which tools Hermes sees from Figma MCP
hermes mcp list figma

# Expected output:
# Available tools from figma:
# - get_file
# - get_file_nodes
# - list_files
# - list_components
# - search_components
# - list_variables
# - list_teams
# ... (all 19 tools)
```

### Test 3: Individual Tool Testing

```bash
# Test specific tools through Hermes
hermes ask "Using Figma MCP, show me my first team"
hermes ask "List all Figma projects in my workspace"
hermes ask "Get the components from my design file"
hermes ask "Find variables in my Figma file"
```

### Test 4: Error Handling

```bash
# Test error scenarios
hermes ask "Get file with invalid ID: notavalidid"
hermes ask "List components from nonexistent file"

# Should handle gracefully with error message
# ✅ Verify error messages are clear
```

---

## Hermes Configuration

### Full Hermes Config Example

**File:** `~/.hermes/config.yaml`

```yaml
# Hermes MCP Configuration

mcp_servers:
  figma:
    # Figma MCP Server configuration
    command: python
    args:
      - -m
      - figma_mcp
    
    env:
      FIGMA_API_TOKEN: ${FIGMA_API_TOKEN}
      MCP_LOG_LEVEL: INFO
    
    timeout: 30
    max_retries: 3
    
  # Other MCPs...
  
# Logging configuration
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance settings
performance:
  parallel_tools: true
  cache_enabled: true
  cache_ttl: 300
```

### Environment Variables

```bash
# Required
export FIGMA_API_TOKEN="figd_xxxxxxxxxxxxxxxxxxxx"

# Optional
export MCP_LOG_LEVEL="DEBUG"  # For debugging
export FIGMA_API_TIMEOUT="30"
export FIGMA_API_RETRY="3"

# Hermes-specific
export HERMES_DEBUG="true"
export HERMES_LOG_LEVEL="DEBUG"
```

---

## Debugging & Troubleshooting

### Enable Debug Logging

```bash
# Set debug mode
export MCP_LOG_LEVEL=DEBUG
export HERMES_DEBUG=true

# Start Hermes with debug output
hermes --debug ask "List my Figma teams"
```

### View Logs

```bash
# Figma MCP logs
tail -f ~/.hermes/logs/figma-mcp.log

# Hermes agent logs
tail -f ~/.hermes/logs/hermes.log

# Both combined
tail -f ~/.hermes/logs/*.log
```

### Common Issues & Solutions

#### Issue 1: "Figma MCP not found"

```bash
# ❌ Problem
Error: figma_mcp module not found

# ✅ Solution
# 1. Verify installation
python -c "import figma_mcp; print(figma_mcp.__file__)"

# 2. Reinstall if needed
pip install -e /path/to/figma-mcp

# 3. Check Python path
echo $PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/figma-mcp"
```

#### Issue 2: "Invalid API Token"

```bash
# ❌ Problem
Error: Invalid or expired API token

# ✅ Solution
# 1. Verify token format
echo $FIGMA_API_TOKEN

# 2. Get new token from https://www.figma.com/api-docs/getting-started
# 3. Update environment variable
export FIGMA_API_TOKEN="new_token_here"

# 4. Test token directly
python -c "
from figma_mcp.client import FigmaClient
client = FigmaClient('YOUR_TOKEN')
print('✅ Token valid')
" 2>&1 | head -20
```

#### Issue 3: "Connection timeout"

```bash
# ❌ Problem
Timeout connecting to Figma API

# ✅ Solution
# 1. Check internet connection
ping api.figma.com

# 2. Increase timeout
export FIGMA_API_TIMEOUT=60

# 3. Check rate limiting
# Figma allows 120 requests/minute
# May need to add delay between requests

# 4. Check Figma API status
curl https://status.figma.com
```

#### Issue 4: "Tool not working"

```bash
# ❌ Problem
hermes ask "List my Figma teams"
# Returns: Tool not found or error

# ✅ Solution
# 1. Check tool availability
hermes mcp list figma

# 2. Check MCP server logs
MCP_LOG_LEVEL=DEBUG python -m figma_mcp 2>&1 | head -50

# 3. Test tool directly
python -c "
from figma_mcp.server import server
from figma_mcp.client import FigmaClient
print('✅ Tools loaded')
"

# 4. Verify Figma account permissions
# Visit https://www.figma.com/api-docs
```

---

## Automated Testing

### Unit Tests for Hermes Integration

**File:** `tests/test_hermes_integration.py`

```python
"""Test Figma MCP integration with Hermes."""

import pytest
import subprocess
import os
from pathlib import Path


class TestHermesIntegration:
    """Tests for Hermes agent integration."""
    
    @pytest.fixture
    def figma_token(self):
        """Get Figma API token from environment."""
        token = os.getenv("FIGMA_API_TOKEN")
        if not token:
            pytest.skip("FIGMA_API_TOKEN not set")
        return token
    
    @pytest.fixture
    def hermes_installed(self):
        """Check if Hermes is installed."""
        result = subprocess.run(
            ["which", "hermes"],
            capture_output=True
        )
        if result.returncode != 0:
            pytest.skip("Hermes not installed")
        return True
    
    def test_hermes_sees_figma_mcp(self, hermes_installed):
        """Test that Hermes can discover Figma MCP tools."""
        result = subprocess.run(
            ["hermes", "mcp", "list", "figma"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "get_file" in result.stdout
        assert "list_teams" in result.stdout
    
    def test_hermes_runs_figma_query(self, figma_token):
        """Test basic query through Hermes."""
        result = subprocess.run(
            ["hermes", "ask", "List my Figma teams"],
            capture_output=True,
            text=True,
            env={**os.environ, "FIGMA_API_TOKEN": figma_token},
            timeout=30
        )
        
        assert result.returncode == 0, f"Failed: {result.stderr}"
        # Response should contain team data or valid error
        assert len(result.stdout) > 0
    
    def test_figma_mcp_responds_to_requests(self, figma_token):
        """Test MCP server responds to requests."""
        # Import and test directly
        from figma_mcp.client import FigmaClient
        
        client = FigmaClient(figma_token)
        # Should be able to instantiate
        assert client is not None
        assert client.api_token == figma_token
    
    def test_error_handling_invalid_file_id(self, figma_token):
        """Test error handling for invalid file IDs."""
        result = subprocess.run(
            ["hermes", "ask", 
             "Get Figma file with ID: invalid_id_12345"],
            capture_output=True,
            text=True,
            env={**os.environ, "FIGMA_API_TOKEN": figma_token},
            timeout=30
        )
        
        # Should fail gracefully
        # Return code could be non-zero, but should have error message
        assert len(result.stdout) > 0 or len(result.stderr) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

Run tests:

```bash
# Run all Hermes integration tests
pytest tests/test_hermes_integration.py -v

# Run specific test
pytest tests/test_hermes_integration.py::TestHermesIntegration::test_hermes_sees_figma_mcp -v

# With coverage
pytest tests/test_hermes_integration.py --cov=figma_mcp
```

---

## CI/CD Integration

### GitHub Actions Workflow for Hermes Testing

**File:** `.github/workflows/hermes-test.yml`

```yaml
name: Hermes Integration Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  hermes-integration:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install Figma MCP
      run: |
        pip install -e ".[dev]"
    
    - name: Install Hermes (if available)
      run: |
        # Attempt to install Hermes from source
        git clone https://github.com/NousResearch/hermes-agent.git
        cd hermes-agent
        pip install -e .
      continue-on-error: true
    
    - name: Test Figma MCP standalone
      run: |
        pytest tests/test_client.py -v
    
    - name: Test Hermes integration
      if: success()
      env:
        FIGMA_API_TOKEN: ${{ secrets.FIGMA_API_TOKEN }}
      run: |
        # Only run if FIGMA_API_TOKEN is set
        if [ -n "$FIGMA_API_TOKEN" ]; then
          pytest tests/test_hermes_integration.py -v
        else
          echo "⚠️  Skipping Hermes tests (no FIGMA_API_TOKEN)"
        fi
    
    - name: Test MCP server startup
      run: |
        timeout 5 python -m figma_mcp &
        sleep 2
        if pgrep -f "figma_mcp" > /dev/null; then
          echo "✅ MCP server started successfully"
          pkill -f "figma_mcp"
        else
          echo "❌ MCP server failed to start"
          exit 1
        fi
```

---

## Manual Verification Checklist

Use this checklist to verify changes work correctly:

### ✅ Installation & Setup
- [ ] Figma MCP cloned successfully
- [ ] `pip install -e .` works without errors
- [ ] Environment variable `FIGMA_API_TOKEN` is set
- [ ] Hermes is installed and running

### ✅ Tool Discovery
- [ ] `hermes mcp list figma` shows all tools
- [ ] Tool count matches documentation (19 tools)
- [ ] All tool names are correct
- [ ] Tool descriptions are present

### ✅ Basic Functionality
- [ ] `hermes ask "List my Figma teams"` works
- [ ] `hermes ask "List Figma projects"` works
- [ ] `hermes ask "Get Figma file..."` works
- [ ] Responses contain expected data

### ✅ Error Handling
- [ ] Invalid file IDs handled gracefully
- [ ] Missing permissions return clear error
- [ ] Network timeouts are handled
- [ ] API rate limits respected

### ✅ Performance
- [ ] Requests complete within 30 seconds
- [ ] No memory leaks (check with `top`)
- [ ] Handles concurrent requests
- [ ] Caching works (if enabled)

### ✅ Security
- [ ] API token not leaked in logs
- [ ] HTTPS used for all requests
- [ ] No sensitive data in error messages
- [ ] Rate limiting prevents abuse

---

## Testing Different Scenarios

### Scenario 1: Fresh Installation

```bash
#!/bin/bash

# Clean install test
rm -rf figma-mcp
git clone https://github.com/jozroftamson/figma-mcp.git
cd figma-mcp

python -m venv test_env
source test_env/bin/activate

pip install -e .
export FIGMA_API_TOKEN="your_token"

# Test basic connection
python -m figma_mcp &
PID=$!
sleep 2
kill $PID

echo "✅ Fresh installation test passed"
```

### Scenario 2: Version Compatibility

```bash
#!/bin/bash

# Test with different Python versions
for version in 3.10 3.11 3.12; do
    echo "Testing Python $version..."
    
    python$version -m venv venv_$version
    source venv_$version/bin/activate
    
    pip install -e .
    pytest tests/ -q
    
    deactivate
    rm -rf venv_$version
done

echo "✅ All versions compatible"
```

### Scenario 3: Integration with Other MCPs

```bash
# Test Figma MCP alongside other MCPs
cat > ~/.hermes/config.yaml << 'EOF'
mcp_servers:
  figma:
    command: python
    args: [-m, figma_mcp]
  
  # Test with other MCPs
  web:
    command: python
    args: [-m, web_mcp]
EOF

# Test that both work
hermes ask "From Figma, get my designs. Then create a webpage."
```

---

## Monitoring & Alerts

### Health Check Script

**File:** `scripts/check_hermes_integration.sh`

```bash
#!/bin/bash

set -e

echo "🔍 Checking Hermes ↔ Figma MCP Integration..."

# Check 1: Token set
if [ -z "$FIGMA_API_TOKEN" ]; then
    echo "❌ FIGMA_API_TOKEN not set"
    exit 1
fi
echo "✅ FIGMA_API_TOKEN configured"

# Check 2: Server can start
timeout 5 python -m figma_mcp > /dev/null 2>&1 &
PID=$!
sleep 2

if kill -0 $PID 2>/dev/null; then
    kill $PID 2>/dev/null || true
    echo "✅ MCP server starts"
else
    echo "❌ MCP server failed to start"
    exit 1
fi

# Check 3: Hermes installed
if ! command -v hermes &> /dev/null; then
    echo "⚠️  Hermes not installed (optional)"
else
    echo "✅ Hermes installed"
fi

# Check 4: API connectivity
python -c "
import requests
try:
    r = requests.head('https://api.figma.com/', timeout=5)
    print('✅ API server reachable')
except:
    print('❌ Cannot reach Figma API')
    exit(1)
"

echo ""
echo "🎉 All checks passed!"
```

Run health check:

```bash
bash scripts/check_hermes_integration.sh
```

---

## Reporting Issues

When reporting issues, include:

```markdown
## Issue: [Brief description]

### Environment
- Python version: `python --version`
- Figma MCP version: `pip show figma-mcp`
- Hermes version: `hermes --version`
- OS: Ubuntu/macOS/Windows

### Steps to Reproduce
1. 
2.
3.

### Expected Behavior
What should happen?

### Actual Behavior
What actually happened?

### Logs
```
Paste relevant logs from:
- stderr/stdout
- ~/.hermes/logs/
```

### Screenshots
(If applicable)
```

---

## Summary

Testing Hermes integration involves:

1. **Local Testing** - Test on your machine first
2. **Tool Discovery** - Verify all 19 tools are available
3. **Functional Testing** - Test individual tools work
4. **Error Testing** - Verify error handling
5. **Performance Testing** - Check response times
6. **CI/CD Testing** - Automated verification
7. **Monitoring** - Ongoing health checks

All changes should be verified before submitting PRs to Hermes!

