# PR Lens Installation Complete ✅

## What's Been Set Up

Your **figma-mcp** project is now ready to use PR Lens for animated architecture diagrams on every pull request.

---

## Files Created

| File | Purpose |
|------|---------|
| `.github/workflows/pr-lens.yml` | GitHub Action to generate diagrams on every PR |
| `.github/pr-lens.yml` | Configuration with component name mappings |
| `PR_LENS_SETUP.md` | Step-by-step installation & configuration guide |
| `PR_LENS_VISUAL_GUIDE.md` | How diagrams look and what they show |

---

## 3 Ways to Use PR Lens

### 1️⃣ GitHub App (Easiest, Recommended)
- **URL**: https://github.com/apps/coldtea-pr-lens
- **Setup**: Click "Install" → Select repo → Done
- **Cost**: Free for public repos
- **Features**: Auto-updating comments with light/dark themes
- **No key needed**: The app brings its own AI

**Next step**: Go to https://github.com/apps/coldtea-pr-lens and install it.

### 2️⃣ GitHub Action (Your Model Key)
- **Setup**: Already configured in `.github/workflows/pr-lens.yml`
- **Cost**: Pay for API calls (~$0.001/PR with Gemini)
- **Supported models**: Gemini, OpenAI, DeepSeek, OpenRouter
- **Setup time**: 2 minutes (add secret, that's it)

**Next step**: 
1. Get an API key: https://aistudio.google.com/app/apikeys (Gemini)
2. Add to GitHub: Settings → Secrets → New repository secret
3. Name it: `GEMINI_API_KEY`
4. Push the workflow (already in repo)

### 3️⃣ Local CLI (Preview Before PR)
- **Command**: `npx @coldtea/pr-lens-cli`
- **Cost**: Free (uses your own key, or mock mode)
- **Use case**: See diagrams locally before opening PR

**Already installed**: `npx @coldtea/pr-lens-cli --version` works

---

## Quick Start

### Option A: Use the GitHub App (Recommended)
```bash
# 1. Install the app
# Go to: https://github.com/apps/coldtea-pr-lens
# Click Install → Select jozrftamson/figma-mcp → Authorize

# 2. Create a test PR
git checkout -b test/pr-lens-demo
echo "# Test" >> figma_mcp/server.py
git add figma_mcp/server.py
git commit -m "Test PR Lens"
git push -u origin test/pr-lens-demo

# 3. Open PR on GitHub
# → Diagram appears in ~30 seconds as a comment
```

### Option B: Use GitHub Action (Your Key)
```bash
# 1. Get API key from https://aistudio.google.com/app/apikeys

# 2. Add to GitHub
# Settings → Secrets and variables → Actions → New repository secret
# Name: GEMINI_API_KEY
# Paste your key

# 3. Workflow is already configured
git add .github/workflows/pr-lens.yml
git commit -m "Add PR Lens GitHub Action"
git push

# 4. Create a PR
# → Diagram appears when Action completes
```

### Option C: Generate Locally
```bash
# Analyze the latest commit
npx @coldtea/pr-lens-cli analyze --base HEAD~1

# Render to SVG
npx @coldtea/pr-lens-cli render .pr-lens/graph.json

# Open
open .pr-lens/*-dark-*.svg  # macOS
firefox .pr-lens/*-dark-*.svg  # Linux
```

---

## What You'll See on Every PR

### The Comment
- **Architecture Diagram**: Shows which files changed and how they connect
- **Data Flow Animation**: Steps through the change with a moving dot
- **Color Coding**: 🟢 green (added), 🟡 amber (changed), 🔴 red (removed)
- **Collapsible Sections**: Details for each component
- **Canvas Link**: Full-size interactive view on prlens.dev

### The Canvas (prlens.dev)
- Full-size, zoomable diagram
- Pan around, explore system architecture
- Click arrows to see data payloads
- Walkthrough mode with animations
- Light/dark theme switching

---

## Configuration

### Component Naming
In `.github/pr-lens.yml`, we've pre-configured names:
```yaml
figma_mcp/server.py → MCP Server
figma_mcp/client.py → Figma API Client
figma_mcp/web_server.py → Web Server (FastAPI)
```

Diagrams will show "MCP Server" instead of "figma_mcp/server.py".

### Customize Names
Edit `.github/pr-lens.yml`:
```yaml
map:
  rename:
    - match: figma_mcp/models.py
      to: Data Models
    - match: tests/
      to: Test Suite
```

### Exclude Files
```yaml
  exclude:
    - "**/*.egg-info"
    - "__pycache__"
    - "venv/"
```

---

## Examples from the Gallery

PR Lens has processed these real PRs:

1. **React Hooks** (2019)
   - https://prlens.dev/gallery/react/react/13968
   - 5 lanes, 36 files, feature flag system

2. **Node.js Fetch API** (2019)
   - https://prlens.dev/gallery/nodejs/node/41749
   - 5 lanes, 16 files, new core feature

3. **Kubernetes Ingress** (2018)
   - https://prlens.dev/gallery/kubernetes/kubernetes/14175
   - 4 lanes, 8 files, new resource type

---

## Support & Docs

- **Website**: https://prlens.dev
- **GitHub**: https://github.com/coldteadotai/pr-lens
- **Discord**: https://discord.gg/nTEFnmBQMJ
- **Twitter**: https://x.com/drawwithlens
- **Detailed Guide**: See `PR_LENS_SETUP.md` and `PR_LENS_VISUAL_GUIDE.md`

---

## Next Steps

### Now (5 minutes)
1. Install the GitHub App: https://github.com/apps/coldtea-pr-lens
2. Create a test PR to see diagrams in action

### Soon (Optional)
1. Add `GEMINI_API_KEY` secret if using GitHub Action
2. Customize `.github/pr-lens.yml` with your component names
3. Ask your coding agent: "Diagram this change with PR Lens"

### Advanced (Later)
1. Use `.github/pr-lens.yml` to organize components into lanes
2. Set up local analysis before creating PRs
3. Integrate with your code review process

---

## TL;DR

**Status**: ✅ Ready to use

**Install**: https://github.com/apps/coldtea-pr-lens

**Test**: Create a test PR → See diagram in comment

**Cost**: Free for public repos (with app); ~$0.001/PR (with your key)

**Diagrams**: Architecture + Data flow + Walkthroughs + Canvas

**Docs**: Read `PR_LENS_SETUP.md` and `PR_LENS_VISUAL_GUIDE.md` in this repo

---

## Questions?

Check `PR_LENS_SETUP.md` for the full FAQ and troubleshooting guide.

