# Example: What PR Lens Posts to Your PR

When you open a pull request, PR Lens automatically generates and posts this comment:

---

## Comment Example

**Posted by: @coldtea-pr-lens Bot** ✓ Just now

### 📊 Architecture Diagram: Fix MCP 2.3.0 Compatibility

<details>
<summary><strong>▼ Full System (4 Components)</strong></summary>

```
┌─────────────────────┐         ┌─────────────────────┐
│  MCP Server         │         │  Web Server         │
│  ━━━━━━━━━━━━━━━   │         │  ━━━━━━━━━━━━━━━   │
│                     │         │                     │
│ 🟢 Update           │         │ ✅ Fix Import       │
│   Decorators        │◄───────►│    (resolved)       │
│                     │         │                     │
│ 🟡 Fix Schema       │         └─────────────────────┘
│   Keys              │
│                     │
│ 🟢 Export TOOLS     │
│   (dict)            │
└─────────────────────┘


┌─────────────────────┐         ┌─────────────────────┐
│  Container          │         │  Config             │
│  ━━━━━━━━━━━━━━━   │         │  ━━━━━━━━━━━━━━   │
│                     │         │                     │
│ 🟡 Security Fix     │         │ 🟢 MyPy Config      │
│   (ARG vs ENV)      │         │   Suppress Errors   │
│                     │         │                     │
│ 🟢 Add Dependencies │         │                     │
│   (FastAPI)         │         │                     │
└─────────────────────┘         └─────────────────────┘
```

**Changes Summary:**
- ✅ 4 files changed
- ✅ 11 additions (green)
- ✅ 2 modifications (amber)
- ✅ 0 removals
- **Status**: All components integrated successfully

</details>

---

### 🎬 Data Flow Animation

<details>
<summary><strong>▶ Play Walkthrough (3 steps)</strong></summary>

**Step 1: Parse Decorators**
```
Input: @server.list_tools()
       ↓
Process: Remove parentheses
       ↓
Output: @server.list_tools
✓ Matches MCP 2.3.0 spec
```

**Step 2: Rename Schema Keys**
```
Input: {
  "inputSchema": {...}
}
       ↓
Process: Convert camelCase → snake_case
       ↓
Output: {
  "input_schema": {...}
}
✓ 19 tool definitions updated
```

**Step 3: Export Module Symbol**
```
Input: # TOOLS dict (hidden)
       ↓
Process: Add to module exports
       ↓
Output: __all__ = ["server", "TOOLS"]
✓ web_server.py can now import
```

</details>

---

### 🔍 Component Details

<details>
<summary><strong>MCP Server Changes (4 items)</strong></summary>

#### 1. Update Decorators
- **File**: `figma_mcp/server.py`
- **Lines**: 30-32, 200
- **Change**: `@server.list_tools()` → `@server.list_tools`
- **Reason**: MCP 2.3.0 uses properties, not decorator functions

#### 2. Fix Schema Keys
- **File**: `figma_mcp/server.py`
- **Lines**: 56-183 (19 locations)
- **Change**: `inputSchema=` → `input_schema=`
- **Reason**: Python naming convention, not JSON schema

#### 3. Add Exports
- **File**: `figma_mcp/server.py`
- **Lines**: 26-30
- **Change**: Added `TOOLS: dict = {}` and `__all__`
- **Reason**: web_server.py needs access to TOOLS

#### 4. Error Handling
- **Type**: Type hints updated to handle new API
- **Result**: ✅ MyPy errors fixed (43 → 0)

</details>

<details>
<summary><strong>Web Server Changes (1 item)</strong></summary>

#### Import Resolution
- **File**: `figma_mcp/web_server.py`
- **Line**: 14
- **Before**: `from figma_mcp.server import TOOLS` ❌ ImportError
- **After**: `from figma_mcp.server import TOOLS` ✅ Works
- **Depends on**: MCP Server export

</details>

<details>
<summary><strong>Docker Changes (2 items)</strong></summary>

#### Security Fix
- **File**: `Dockerfile`
- **Lines**: 32-33
- **Change**: `ENV FIGMA_API_TOKEN=""` → `ARG FIGMA_API_TOKEN`
- **Benefit**: Token no longer exposed in image history

#### Add Dependencies
- **File**: `Dockerfile`
- **Lines**: 14-16
- **Change**: Copy + install `requirements-web.txt`
- **Added**: FastAPI, Uvicorn (for web server mode)

</details>

<details>
<summary><strong>Configuration Changes (1 item)</strong></summary>

#### MyPy Configuration
- **File**: `pyproject.toml`
- **Change**: Added `[tool.mypy]` section
- **Settings**:
  - `ignore_missing_imports = true` (MCP library stubs)
  - `disallow_untyped_defs = false` (allow inference)
- **Result**: Type checking now passes

</details>

---

### 📈 Metrics

| Metric | Value |
|--------|-------|
| **Files Changed** | 4 |
| **Lines Added** | 47 |
| **Lines Modified** | 13 |
| **Lines Removed** | 0 |
| **Components Affected** | 4 lanes |
| **Test Coverage** | ✅ 3/3 passing |
| **Build Status** | ✅ Docker build success |

---

### 🔗 Full Interactive Canvas

View the diagram at full size with zoom, pan, and animations:

📐 **[Open on prlens.dev →](https://prlens.dev/c/example-id-here)**

(This link shows the diagram with full interactivity. You can pan around, zoom in, click arrows to see payloads, and play the walkthrough animation.)

---

### 📝 Reviewers' Checklist

- [ ] Architecture changes reviewed
- [ ] Data flow makes sense
- [ ] No unexpected dependencies
- [ ] Component names are accurate
- [ ] All lanes are accounted for

---

**🎯 Key Insight**: All four components integrate properly. The MCP Server exports the TOOLS dict that the Web Server imports. Docker is secured and includes all dependencies. Configuration adjusts for the new MCP API. The system is ready.

---

*Generated by PR Lens · [Learn more](https://prlens.dev)*

