# PR Lens Setup Guide for figma-mcp

## ✅ What's Been Set Up

### 1. GitHub Action Workflow
- **File**: `.github/workflows/pr-lens.yml` (created)
- **Trigger**: Automatically runs on every pull request
- **Function**: Analyzes code changes and posts animated architecture diagrams as PR comments
- **Updates**: Automatically updates the comment on each new push to the PR

### 2. PR Lens Configuration
- **File**: `.github/pr-lens.yml` (created)
- **Purpose**: Maps file names to human-readable component names
- **Benefits**: Diagrams show "MCP Server" instead of "figma_mcp/server.py"

### 3. Naming Mappings (Configured)
```
figma_mcp/server.py        → MCP Server
figma_mcp/client.py        → Figma API Client
figma_mcp/web_server.py    → Web Server (FastAPI)
Dockerfile                 → Container Config
pyproject.toml             → Python Dependencies
tests/                     → Test Suite
```

---

## 📋 Next Steps: Install GitHub App

### Step 1: Install the PR Lens GitHub App
1. Go to: **https://github.com/apps/coldtea-pr-lens**
2. Click **"Install"**
3. Select your repository: **jozrftamson/figma-mcp** (or all your repositories)
4. Authorize the installation

The app requires these permissions:
- **Read**: Code, Pull Requests (to analyze changes)
- **Write**: Pull Request comments (to post diagrams)

**Note**: The App is **free for public repositories** and open source projects.

### Step 2 (Optional): Use GitHub Action Instead

If you prefer to use your own model key instead of the hosted app:

1. **Generate an API Key**:
   - **Gemini** (recommended): https://aistudio.google.com/app/apikeys
   - **OpenAI**: https://platform.openai.com/api/keys
   - **DeepSeek** or **OpenRouter**: Their respective dashboards

2. **Add Secret to GitHub**:
   - Go to: Settings → Secrets and variables → Actions
   - Click **"New repository secret"**
   - Name: `GEMINI_API_KEY` (or `OPENAI_API_KEY` for OpenAI)
   - Value: Paste your API key
   - Click **"Add secret"**

3. **Modify Workflow** (if using OpenAI instead of Gemini):
   ```yaml
   - uses: coldteadotai/pr-lens/packages/action@v0
     with:
       api-key: ${{ secrets.OPENAI_API_KEY }}
       provider: openai  # Add this line
   ```

4. **Push the workflow file**:
   ```bash
   git add .github/workflows/pr-lens.yml
   git commit -m "Add PR Lens GitHub Action"
   git push
   ```

---

## 🎬 How It Works

### Via GitHub App (Recommended)
- **Setup**: Install app → one-time configuration
- **Cost**: Free for public repos; per-PR cost for private repos
- **Features**: 
  - ✅ Animated diagrams
  - ✅ Auto-updating comments
  - ✅ Light/dark theme switching
  - ✅ Interactive canvas links
  - ✅ Checkboxes for reviewers

### Via GitHub Action (Your Key)
- **Setup**: Generate API key → add secret → commit workflow
- **Cost**: Pay for your API calls (Gemini is cheap; ~$0.001 per PR)
- **Features**:
  - ✅ Animated diagrams (Gemini/OpenAI)
  - ✅ Posted on every push
  - ⚠️ No auto-updating checkboxes (GitHub Action limitation)

---

## 🧪 Test the Setup

### Option A: Create a Test Pull Request
1. Create a branch:
   ```bash
   git checkout -b test/pr-lens-demo
   ```

2. Make a small change to a Python file:
   ```bash
   echo "# Test change" >> figma_mcp/server.py
   git add figma_mcp/server.py
   git commit -m "Test PR Lens diagram"
   git push -u origin test/pr-lens-demo
   ```

3. Open a pull request on GitHub

4. **Watch the magic**:
   - If using the **GitHub App**: Diagram appears in ~30 seconds
   - If using the **GitHub Action**: Diagram appears when CI completes
   - The diagram shows the changed file with architecture and data flow

### Option B: Generate Locally (No Key Required)
Generate a diagram on your computer to preview:
```bash
cd /tmp/figma-mcp

# Analyze the latest commit
npx @coldtea/pr-lens-cli analyze --base HEAD~1

# Render to SVG (uses the analysis data)
npx @coldtea/pr-lens-cli render .pr-lens/graph.json

# Open the diagram
open .pr-lens/*-dark-*.svg  # macOS
# or
firefox .pr-lens/*-dark-*.svg  # Linux
```

---

## 📊 What You'll See

### On Every Pull Request:
1. **Architecture Diagram**:
   - Shows which files/components changed
   - Color-coded: **Green** (new), **Amber** (modified), **Red** (deleted)
   - Animated arrows showing data flow

2. **Data Flow Walkthrough**:
   - Step-by-step animation of how data moves through changed code
   - Click arrows to see payload details

3. **Zoom-In Views**:
   - Collapsible sections for each changed component
   - Full system diagram + individual component close-ups

4. **Interactive Canvas**:
   - Link to `prlens.dev` for full-size, interactive exploration
   - Pan, zoom, light/dark theme, walkthrough animations

---

## 🔧 Configuration Details

### In `.github/pr-lens.yml`:

**Rename Components**:
```yaml
map:
  rename:
    - match: pattern/to/match
      to: Human Readable Name
```

**Exclude Files**:
```yaml
  exclude:
    - "**/*.test.ts"      # All test files
    - "*.lock"            # Lock files
    - "node_modules/**"   # Dependencies
```

**Pin Components to Lanes**:
```yaml
  lanes:
    - name: "Frontend"
      include:
        - "src/web/**"
    - name: "Backend"
      include:
        - "src/api/**"
```

For all options, see: https://github.com/coldteadotai/pr-lens/blob/main/packages/cli#repository-config

---

## 🤖 Using PR Lens with Your Coding Agent

If you have a coding agent (Claude, Copilot, etc.), install the skill:

```bash
npx skills add coldteadotai/pr-lens
```

Then ask your agent:
> "Before opening a PR, diagram this change with PR Lens and attach it to the pull request description."

The agent will:
1. Analyze your code changes
2. Generate architecture & data-flow diagrams
3. Create an SVG rendering
4. Add the diagram to your PR before you even open it

---

## 📚 Examples

### React Hooks PR (from PR Lens gallery)
- 5 files changed, 5 lanes of architecture
- **View**: https://prlens.dev/gallery/react/react/13968

### Node.js fetch PR (from PR Lens gallery)
- 16 files changed, 5 lanes of architecture
- **View**: https://prlens.dev/gallery/nodejs/node/41749

### Kubernetes Ingress PR (from PR Lens gallery)
- 8 files changed, 4 lanes of architecture
- **View**: https://prlens.dev/gallery/kubernetes/kubernetes/14175

---

## ❓ FAQ

**Q: Do I need to provide my own API key?**
A: No for the GitHub App (free). Yes for the GitHub Action (but cheap: ~$0.001/PR with Gemini).

**Q: Which model should I use?**
A: Gemini is recommended (fastest, cheapest). OpenAI works too. DeepSeek/OpenRouter also supported via `--provider openai-compatible --base-url <url>`.

**Q: Can I use this in private repositories?**
A: Yes. GitHub App costs per PR. GitHub Action uses your own key (cheaper).

**Q: Does PR Lens modify my code?**
A: No. It only analyzes diffs and generates SVG diagrams. No code changes.

**Q: Can I run this locally?**
A: Yes. Use the CLI: `npx @coldtea/pr-lens-cli analyze` and `render`.

**Q: Can I use this with GitLab or Bitbucket?**
A: Yes. PR Lens supports all three. See https://prlens.dev/gitlab or https://prlens.dev/bitbucket.

---

## 🚀 Recommended Flow

1. **Immediate**: Install GitHub App → Start getting diagrams on all PRs
2. **Optional**: Configure `.github/pr-lens.yml` if names are wrong
3. **Advanced**: Use GitHub Action if you want to control the model/cost
4. **Local**: Use CLI for local analysis before pushing

---

## Files Created

- **`.github/workflows/pr-lens.yml`**: GitHub Action workflow (GitHub-only trigger)
- **`.github/pr-lens.yml`**: Configuration with component name mappings
- **`.pr-lens/`**: Generated diagrams (auto-added to .gitignore)

---

## Support & Resources

- **Website**: https://prlens.dev
- **Docs**: https://github.com/coldteadotai/pr-lens
- **Discord**: https://discord.gg/nTEFnmBQMJ
- **Twitter**: https://x.com/drawwithlens

