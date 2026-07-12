# 🚀 Railway Deployment Guide - Figma MCP Server

Schritt-für-Schritt Guide um Figma MCP Server heute zu Railway zu deployen.

---

## ⚡ Quick Start (5 Minuten)

### Schritt 1: Railway Account erstellen
```bash
# Gehe zu https://railway.app
# Click "Sign Up"
# Connect mit GitHub (easiest)
# Authorize Railway
```

### Schritt 2: Railway CLI installieren
```bash
# macOS
brew install railway

# Linux
curl -fsSL https://railway.app/install.sh | bash

# Windows
# Download: https://github.com/railwayapp/cli/releases
```

### Schritt 3: Authentifizieren
```bash
railway login
# Opens browser for authentication
# Paste token when prompted
```

### Schritt 4: Deploy Figma MCP
```bash
cd /tmp/figma-mcp-server
railway init

# Choose "Create a new project"
# Name: "figma-mcp"
# Select Python as language
```

### Schritt 5: Configure Environment
```bash
# Add environment variable
railway variables set FIGMA_API_TOKEN="your_token_here"

# Or via Railway dashboard:
# Project Settings → Variables → Add
```

### Schritt 6: Deploy
```bash
railway up

# Or via dashboard:
# Click "Deploy" button
```

### Schritt 7: Get Public URL
```bash
railway open
# Shows your live URL
```

**DONE! Your server is LIVE** 🎉

---

## 📋 Detailed Setup

### Prerequisites
```bash
# Check you have these:
python --version        # 3.10+
pip --version          # pip
git --version          # git
```

### Railway Project Setup

```bash
# 1. Create Procfile (Railway needs this)
cat > /tmp/figma-mcp-server/Procfile << 'EOF'
web: python -m figma_mcp.server
EOF

# 2. Create runtime.txt (specify Python version)
cat > /tmp/figma-mcp-server/runtime.txt << 'EOF'
python-3.11.7
EOF

# 3. Create .railwayignore (exclude unnecessary files)
cat > /tmp/figma-mcp-server/.railwayignore << 'EOF'
.git
.gitignore
.pytest_cache
__pycache__
*.pyc
.env.local
.vscode
.idea
*.md
tests/
docs/
.github/
EOF

# 4. Commit changes
cd /tmp/figma-mcp-server
git add Procfile runtime.txt .railwayignore
git commit -m "Add Railway deployment config"
git push origin master
```

### Railway Web Interface Setup

```
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Authorize GitHub if needed
5. Select: jozroftamson/figma-mcp
6. Railway auto-deploys on push!
```

### Environment Variables

In Railway Dashboard:
```
Project Settings → Variables → Add

FIGMA_API_TOKEN = figd_xxxxxxxxxxxxx
MCP_LOG_LEVEL = INFO
PYTHONUNBUFFERED = 1
```

### Port Configuration

Railway automatically:
- Assigns PORT env var (default 8000)
- Exposes on public URL
- Handles SSL/HTTPS

Your app should listen on PORT env var:
```python
# In server.py
import os
port = int(os.getenv("PORT", 8000))
```

---

## 🔧 Make Server HTTP-Compatible

Your MCP server needs to be callable via HTTP. Create a wrapper:

```python
# File: figma_mcp/web_server.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio

from figma_mcp.server import TOOLS, figma_client

app = FastAPI(title="Figma MCP Server")

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Figma MCP Server",
        "tools": len(TOOLS),
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Railway health check."""
    return {"status": "ok"}

@app.get("/tools")
async def list_tools():
    """List all available tools."""
    return {
        "tools": list(TOOLS.keys()),
        "count": len(TOOLS)
    }

@app.post("/call_tool")
async def call_tool_endpoint(tool_name: str, **kwargs):
    """Call a tool via HTTP."""
    if tool_name not in TOOLS:
        raise HTTPException(
            status_code=404,
            detail=f"Tool {tool_name} not found"
        )
    
    try:
        tool_func = TOOLS[tool_name]
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(**kwargs)
        else:
            result = tool_func(**kwargs)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Example specific endpoints
@app.get("/api/teams")
async def get_teams():
    """Get all teams."""
    try:
        teams = await figma_client.list_teams()
        return {"teams": teams}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/file/{file_key}")
async def get_file(file_key: str):
    """Get file details."""
    try:
        file_data = await figma_client.get_file(file_key)
        return {"file": file_data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Update Procfile

```bash
cat > /tmp/figma-mcp-server/Procfile << 'EOF'
web: python -m figma_mcp.web_server
EOF

# Add fastapi & uvicorn to dependencies
echo "fastapi>=0.104.0" >> /tmp/figma-mcp-server/requirements-web.txt
echo "uvicorn[standard]>=0.24.0" >> /tmp/figma-mcp-server/requirements-web.txt

# Update pyproject.toml
```

---

## 📦 Update pyproject.toml

```toml
[project]
name = "figma-mcp"
version = "1.0.0"
description = "Figma MCP Server - Model Context Protocol integration"
dependencies = [
    "httpx>=0.25.0",
    "pydantic>=2.0",
    "aiohttp>=3.8.0",
    # Web server dependencies (for Railway deployment)
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
    "bandit>=1.7.0",
]

web = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "python-multipart>=0.0.6",
]
```

---

## 🚀 Complete Deployment Steps

### Step 1: Prepare Project
```bash
cd /tmp/figma-mcp-server

# 1. Create web server
cat > figma_mcp/web_server.py << 'EOF'
# (use the code from above)
EOF

# 2. Update Procfile
echo "web: python -m figma_mcp.web_server" > Procfile

# 3. Create runtime.txt
echo "python-3.11.7" > runtime.txt

# 4. Update dependencies
pip install fastapi uvicorn
```

### Step 2: Test Locally
```bash
# Make sure it works locally first
PORT=8000 python -m figma_mcp.web_server

# In another terminal:
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/tools
```

### Step 3: Commit & Push
```bash
git add -A
git commit -m "Add web server for Railway deployment

- FastAPI HTTP wrapper for MCP server
- All tools accessible via REST API
- Health check endpoints
- CORS enabled for browser access
- Ready for Railway deployment"
git push origin master
```

### Step 4: Railway Setup
```bash
# Install Railway CLI
brew install railway  # or your OS equivalent

# Login to Railway
railway login

# Go to Railway Dashboard
# https://railway.app/dashboard

# Click "New Project"
# Select "Deploy from GitHub"
# Select: jozroftamson/figma-mcp
# Railway auto-connects & deploys!
```

### Step 5: Configure Environment
In Railway Dashboard:
```
1. Click your project
2. Click "figma-mcp" service
3. Go to "Variables"
4. Add: FIGMA_API_TOKEN = your_token_here
5. Click "Redeploy"
```

### Step 6: Get Your Public URL
```
In Railway Dashboard:
1. Click "figma-mcp" service
2. Look for "Deployments"
3. Click the latest deployment
4. Copy the "Domain" URL
5. Test: curl https://your-domain.railway.app/health
```

---

## 📡 Testing Your Deployment

```bash
# Get your Railway URL (from dashboard or CLI)
RAILWAY_URL="https://your-domain.railway.app"

# Test health check
curl $RAILWAY_URL/health

# Test tools list
curl $RAILWAY_URL/tools

# Test get teams
curl "$RAILWAY_URL/api/teams"

# Test with file key
curl "$RAILWAY_URL/api/file/YOUR_FIGMA_FILE_KEY"
```

---

## 🎯 What You'll Get

After deployment:

```
✅ Live URL: https://figma-mcp-XXXXX.railway.app
✅ Health Check: /health endpoint
✅ Tools List: /tools endpoint  
✅ Teams API: /api/teams
✅ File API: /api/file/{key}
✅ HTTP Access: Full REST API
✅ Auto-HTTPS: Railway handles SSL
✅ Auto-Scaling: Railway manages load
✅ Public IP: Share with anyone
```

---

## 📋 Deployment Checklist

```
□ Railway account created
□ Railway CLI installed & authenticated
□ Procfile created
□ runtime.txt created
□ Web server code created
□ Dependencies updated
□ Local test successful
□ Changes committed & pushed
□ Railway project created
□ Environment variables set
□ Deployment successful
□ Public URL tested
□ Health check working
□ API endpoints responding
```

---

## 🎉 After Deployment

### Update README
```markdown
## Try It Live!

**Live Demo:** https://figma-mcp-XXXXX.railway.app

### Quick Test

```bash
# Get health status
curl https://figma-mcp-XXXXX.railway.app/health

# List available tools
curl https://figma-mcp-XXXXX.railway.app/tools

# Get your Figma teams
curl https://figma-mcp-XXXXX.railway.app/api/teams
```
```

### Share the URL
- GitHub README
- Twitter/LinkedIn
- Product Hunt
- Dev.to
- HackerNews

---

## 🔗 Next Steps

### Immediate
```
1. Deploy successfully
2. Test the API
3. Update README with live URL
4. Share with GitHub followers
```

### Short-term
```
1. Record demo video using live URL
2. Write blog post with live demo
3. Post on Dev.to/HackerNews
4. Tweet announcement
```

### Medium-term
```
1. Build CLI tool
2. Find early adopters
3. Build React code generation
4. Launch SaaS (Stripe)
```

---

## 🆘 Troubleshooting

### Deployment Failed
```
Check Railway Dashboard:
1. Go to "Deployments"
2. Click failed deployment
3. View logs
4. Common issues:
   - Missing FIGMA_API_TOKEN
   - Port not set correctly
   - Python version mismatch
```

### API Not Responding
```
1. Check /health endpoint
2. View deployment logs
3. Verify FIGMA_API_TOKEN is set
4. Check Railway status page
```

### Port Issues
```
Railway sets PORT env var automatically.
Make sure your server reads it:

port = int(os.getenv("PORT", 8000))
```

---

## 📚 Reference

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- GitHub Pages: https://github.com/railwayapp/cli

---

## ✨ You're Live!

After deployment:
- Your server is accessible globally
- API can be called from anywhere
- Ready for integrations
- Ready for growth

**CONGRATULATIONS!** 🎉

