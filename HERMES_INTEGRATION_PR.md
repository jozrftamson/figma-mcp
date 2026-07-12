# 🔗 Figma MCP Server - Integration mit Hermes

## PR für: NousResearch/hermes-agent

**Titel:** Add Figma MCP Server to ecosystem recommendations

**Description:**

Als Nachfolge zu PR #9857 (figma-prompt-hub) wird hiermit ein **standalone Figma MCP Server** als recommended integration vorgestellt.

### 📋 Summary

Das Projekt `figma-mcp` ist ein produktionsreifer MCP Server für die Figma API, der direkt mit Hermes integriert werden kann:

- ✅ **19 MCP-Tools** für Figma API
- ✅ **Hermes Integration Ready** (config + setup guide)
- ✅ **Produktionsreifer Code** mit Tests, Type Hints, Docstrings
- ✅ **MIT Open Source License**
- ✅ **Vollständige Dokumentation**

### 🎯 Warum relevance?

Adressiert den ursprünglichen Wunsch von #9857 auf die richtige Way:
- Nicht im core tree (per standing policy)
- Standalone repository
- MCP-basiert (wie Hermes empfiehlt)
- Community-maintained

### 🔗 Links

- **Repository:** https://github.com/jozrftamson/figma-mcp
- **Features:** README.md im Repo
- **Setup Guide:** CONTRIBUTING.md im Repo

### 📝 Wo Hermes documentation aufgreifen könnte:

1. **MCP Examples Docs** - Als Beispiel für custom MCP Server
2. **Plugin/Integration Guide** - Alternative zu in-tree Integrationen
3. **Community Resources** - Link zur Figma MCP im Ökosystem

---

**File to add or update:**

Optionale Datei für Hermes: `docs/integrations/community-mcp-servers.md`

```markdown
# Community MCP Servers

Recommended standalone MCP servers für Hermes integration:

## Figma MCP Server

**Repository:** https://github.com/jozrftamson/figma-mcp

MCP server für Figma API integration mit Hermes.

### Features

- 19 MCP tools für file, component, variable, team operations
- Hermes config examples
- Full documentation

### Setup

```bash
pip install git+https://github.com/jozrftamson/figma-mcp.git
hermes mcp add figma --command python --args -m figma_mcp
```

See repository for full documentation.
```

---

### Nicht breaking, nur informativ

- Keine changes an Hermes core
- Nur documentation/recommendation
- User können optional integrieren

### Related

- Closes ecosystem gap von #9857
- Demonstrates best practice MCP integration pattern
