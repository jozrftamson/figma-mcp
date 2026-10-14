# PR Lens Visual Guide - figma-mcp Deployment Fixes

## What Diagrams Look Like

PR Lens generates **animated architecture and data-flow diagrams** for every pull request. Here's what you'll see:

---

## Example: Deployment Readiness Fixes PR

### Layout Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                     PULL REQUEST COMMENT                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  📊 Architecture Diagram (4 lanes of changes)                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                   │
│  Lane 1: MCP Server                                              │
│  ┌──────────────────┐                                            │
│  │🟢 Update         │                                            │
│  │ Decorators       │──────────┐                                │
│  └──────────────────┘          │                                │
│                                 ▼                                │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │🟡 Fix Schema    │  │🟢 Export TOOLS   │                    │
│  │ Keys            │  │ (new)            │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                   │
│  Lane 2: Web Server                                              │
│  ┌──────────────────┐                                            │
│  │✅ Fix Import    │ ◄── Depends on Lane 1                     │
│  │ (no longer err)  │                                            │
│  └──────────────────┘                                            │
│                                                                   │
│  Lane 3: Container (Docker)                                      │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │🟡 Security Fix   │  │🟢 Add Deps       │                    │
│  │ (ARG not ENV)    │  │ (FastAPI)        │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                   │
│  Lane 4: Configuration                                           │
│  ┌──────────────────┐                                            │
│  │🟢 MyPy Config    │                                            │
│  │ (suppress errs)  │                                            │
│  └──────────────────┘                                            │
│                                                                   │
│  🎬 Data Flow Animation                                          │
│  ─────────────────────────────────────────────────────────────  │
│  [Play] Steps through the change 1 → 2 → 3 with moving dot     │
│                                                                   │
│  🔧 Details Sections                                            │
│  <details>                                                        │
│  <summary>► MCP Server Changes</summary>                        │
│  [Individual diagram for this lane]                             │
│  </details>                                                      │
│                                                                   │
│  <details>                                                        │
│  <summary>► Removed Code (Diff Revert)</summary>                │
│  [Shows what was removed if applicable]                         │
│  </details>                                                      │
│                                                                   │
│  📐 Canvas Link                                                  │
│  [View full-size interactive diagram on prlens.dev]             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Color Coding

| Color  | Meaning          | Example                          |
|--------|------------------|----------------------------------|
| 🟢 Green | **Added/New** | Export TOOLS dict (didn't exist) |
| 🟡 Amber | **Changed** | `inputSchema` → `input_schema`  |
| 🔴 Red  | **Removed** | (none in this PR)                |

---

## What Each Card Shows

### Card Example: "Update Decorators"
```
┌─────────────────────────────────────┐
│ 🟢 Update Decorators                │  ← Card title (color = status)
├─────────────────────────────────────┤
│ @server.list_tools() →              │  ← What changed
│ @server.list_tools                  │
├─────────────────────────────────────┤
│ Removed parentheses from            │  ← Description of why
│ decorator syntax to match            │
│ MCP 2.3.0 API                        │
│                                      │
│ Files: figma_mcp/server.py           │  ← Which files affected
│ Line: 30                              │
└─────────────────────────────────────┘
```

---

## Interactive Features

### Click on Arrows
```
Update Decorators ──────→ Fix Schema Keys
       ↓
[Click arrow to see:]
{
  "reason": "Both changes required for MCP 2.3.0 compatibility",
  "flow": "Schema validation depends on correct decorator syntax",
  "payload": {
    "Tool": { "input_schema": {...} }  ← New field (green)
  }
}
```

### Fold/Unfold Sections
```
<details>
<summary>▶ MCP Server Changes (3 items)</summary>

[Expanded view with detailed diagram for just the server.py changes]

</details>
```

### Animation Playback
```
Press [Play] or press 'W' to walk through the change:

Step 1: Decorator syntax updated (0.5s)
Step 2: Schema keys renamed (0.5s)
Step 3: TOOLS exported (0.5s)

[Animated dot moves through each step]
```

---

## Mobile / Light vs Dark Theme

GitHub automatically shows the right version:

### Light Theme (GitHub default)
- White background with black text
- Gray boxes, green/amber/red accents
- High contrast for visibility

### Dark Theme (GitHub dark mode)
- Dark background with light text
- Slightly different gray, same colors
- Renders automatically by GitHub

---

## Full-Size Canvas View

PR Lens generates a link to **prlens.dev** for the full interactive view:

```
📐 View on Canvas: https://prlens.dev/c/uSdxMcPBFwhfgfaGh-dveQ
```

When you click it:
- **Full-size diagram** with unlimited zoom
- **Pan around** the entire architecture
- **Hover cards** to see details
- **Click arrows** to inspect data payloads
- **Toggle light/dark** theme
- **Walkthrough mode** plays animations step by step

---

## Behind the Scenes

### What PR Lens Analyzes

For each PR, it reads:
1. **The diff** (what code changed)
2. **File dependencies** (which files call which)
3. **Type hints & imports** (what data flows between them)
4. **Your .github/pr-lens.yml** (custom names & exclusions)

### What It Sends to the Model

- The **diff** (code changes)
- **File structure** (which files exist)
- **Type hints** (what types flow between files)
- **Your configuration** (rename rules)

**Not sent**: Your entire codebase, tests, or secrets.

### The Model Determines

- Which components are involved
- How they're connected
- What data flows between them
- Labels for each lane
- What changed: added/modified/removed

### What Gets Rendered

1. **Architecture Diagram**
   - Boxes = components/files
   - Arrows = function calls / dependencies
   - Colors = change status

2. **Data Flow**
   - Animated step-by-step walkthrough
   - Shows payload at each step
   - Highlights new/removed fields

3. **Diff Details**
   - Side-by-side: what's new, what's gone
   - Color-coded: green (added), red (removed)

---

## Example Payload Inspection

Click an arrow in the diagram to see:

```
Request Payload:
{
  "file_key": "abc123xyz",
  "version": null          ← New field (green)
}

Response:
{
  "result": {
    "name": "My File",
    "key": "abc123xyz"
  },
  "error": null           ← Removed in new version (red)
}
```

---

## Local Test: Generate Locally

See diagrams on your machine before the PR:

```bash
# Analyze the last 2 commits
npx @coldtea/pr-lens-cli analyze --base HEAD~2

# Render to SVG (light + dark versions)
npx @coldtea/pr-lens-cli render .pr-lens/graph.json

# Open the diagram
open .pr-lens/*-dark-*.svg  # macOS
# or
firefox .pr-lens/*-dark-*.svg  # Linux
# or
start .pr-lens/*-dark-*.svg  # Windows
```

Output files:
```
.pr-lens/
├── graph.json                    ← Raw analysis data
├── manifest.json                 ← Comment metadata
├── my-change-light-*.svg         ← Light theme SVG
└── my-change-dark-*.svg          ← Dark theme SVG
```

---

## What's Stored Where

### In GitHub (Permanent)
- **PR comment** with embedded SVGs
- **Canvas link** to prlens.dev (archived version)

### In prlens.dev (Searchable)
- Gallery of all public PR diagrams
- Searchable by repo, author, date
- Example: https://prlens.dev/gallery/react/react/13968

### In Your Repo (Temporary)
- `.pr-lens/` folder (auto-added to .gitignore)
- Rebuilds from diff anytime you run the CLI
- Safe to delete

---

## Advanced: Custom Corrections

If the model names something wrong, fix it in `.github/pr-lens.yml`:

```yaml
map:
  rename:
    - match: "src/utils/api-client.ts"
      to: "HTTP Client"
    - match: "services/auth"
      to: "Auth Service"

  exclude:
    - "**/*.test.ts"
    - "node_modules/**"
    
  lanes:
    - name: "Frontend"
      include: ["src/ui/**", "src/web/**"]
    - name: "API"
      include: ["src/api/**", "services/**"]
```

These rules persist even if the model changes its analysis.

---

## FAQ About Diagrams

**Q: Can I edit the diagram?**
A: No, diagrams are generated from code. Edit the `.github/pr-lens.yml` config instead.

**Q: Does the diagram show my secrets?**
A: No, PR Lens only sees the diff and file structure. Secrets are never shown.

**Q: What if I have no dependencies between files?**
A: PR Lens still shows each file as a separate card, but no arrows connecting them.

**Q: Can I run this offline?**
A: Yes, with the CLI and a local model (Ollama). See the README.

**Q: What if the diagram is wrong?**
A: Use `.github/pr-lens.yml` to rename, reorganize, or exclude files.

---

## Example PRs to Explore

From the PR Lens gallery (real PRs, real diagrams):

1. **React Hooks** (Complex)
   - https://prlens.dev/gallery/react/react/13968
   - 36 files, 5 lanes, feature flag implementation

2. **Node.js Fetch** (Medium)
   - https://prlens.dev/gallery/nodejs/node/41749
   - 16 files, 5 lanes, adding fetch to Node core

3. **Kubernetes Ingress** (Simple)
   - https://prlens.dev/gallery/kubernetes/kubernetes/14175
   - 8 files, 4 lanes, new resource type

---

## Next: Set Up for Your Project

1. **Install GitHub App**: https://github.com/apps/coldtea-pr-lens
2. **Optionally configure**: Edit `.github/pr-lens.yml` if needed
3. **Create a test PR**: See the diagram appear automatically
4. **Share with your team**: Everyone sees diagrams on every PR going forward

---

**Ready?** Follow the steps in `PR_LENS_SETUP.md` to get started!

