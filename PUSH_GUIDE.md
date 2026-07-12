# 🚀 Figma MCP Server - Push zu GitHub

## Step-by-Step Guide zum Veröffentlichen

### Voraussetzungen
- ✅ Git installiert
- ✅ GitHub Account
- ✅ SSH-Keys konfiguriert (optional, aber empfohlen)

### 1️⃣ GitHub Repository erstellen

**Option A: Mit GitHub CLI**
```bash
# GitHub CLI installieren: https://cli.github.com/
gh auth login

# Repo erstellen
gh repo create figma-mcp \
  --public \
  --description "Figma MCP Server - Model Context Protocol integration for Figma API" \
  --homepage "https://github.com/yourusername/figma-mcp#readme"

# Output:
# ✓ Created repository yourusername/figma-mcp
# git remote add origin https://github.com/yourusername/figma-mcp.git
```

**Option B: Web UI (https://github.com/new)**
- Name: `figma-mcp`
- Description: "Figma MCP Server - Model Context Protocol integration"
- Public
- Add README (optional - wir haben schon einen)
- Add LICENSE (optional - wir haben schon eine)
- Add .gitignore (optional - wir haben schon einen)

### 2️⃣ Remote hinzufügen und pushen

```bash
cd /tmp/figma-mcp-server

# Remote konfigurieren (ersetze USERNAME mit deinem GitHub-Username)
git remote add origin https://github.com/USERNAME/figma-mcp.git

# Branch umbenennen zu 'main'
git branch -M main

# Code pushen
git push -u origin main
```

**Output:**
```
Zähle Objekte auf: 13, erledigt.
Komprimiere Objekte: 100% (12/12), erledigt.
Schreibe Objekte: 100% (13/13), 45 KiB | 1.50 MiB/s, erledigt.
Gesamt 13 (Delta 0), wiederverwendet 0 (Delta 0), wiederverwendet 0 (Diff: 0)
To https://github.com/USERNAME/figma-mcp.git
 * [new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

### 3️⃣ Verifizieren

```bash
# Remote überprüfen
git remote -v
# Output:
# origin  https://github.com/USERNAME/figma-mcp.git (fetch)
# origin  https://github.com/USERNAME/figma-mcp.git (push)

# Branch überprüfen
git branch -a
# Output:
# * main
#   remotes/origin/main

# Commits checken
git log --oneline
# Output:
# 2b3009b Add deployment documentation
# c83b00c Initial commit: Figma MCP Server
```

### 4️⃣ GitHub Repo konfigurieren

**Repository Settings anpassen:**

1. **Topics** (Labels)
   - `mcp`
   - `figma`
   - `model-context-protocol`
   - `hermes`
   - `python`
   - `api-client`

2. **About** Sektion
   - Description: "Figma MCP Server for Hermes AI Agent"
   - Website: (optional)
   - Topics: siehe oben

3. **Branches**
   - Default Branch: `main`
   - Branch Protection: Optional
     - Require pull request reviews: Nein (für kleine Projekte)
     - Require status checks: Nein
     - Require branches to be up to date: Nein

4. **Actions** (optional)
   - Workflows können später hinzugefügt werden

### 5️⃣ Optional: GitHub Actions CI/CD

Erstelle `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [ '3.10', '3.11', '3.12' ]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    - name: Lint with ruff
      run: ruff check figma_mcp/
    - name: Type check with mypy
      run: mypy figma_mcp/
    - name: Test with pytest
      run: pytest tests/ -v
```

Dann pushen:
```bash
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI"
git push
```

### 6️⃣ Optional: Releases & Tags

```bash
# Tag erstellen
git tag -a v0.1.0 -m "Initial release: Figma MCP Server v0.1.0"

# Tag pushen
git push origin v0.1.0

# Release auf GitHub erstellen
gh release create v0.1.0 \
  --title "Figma MCP Server v0.1.0" \
  --notes "First stable release with complete Figma API integration"
```

### 7️⃣ Optional: PyPI Veröffentlichung

**a) Build Tools installieren**
```bash
pip install build twine
```

**b) Bauen**
```bash
cd /tmp/figma-mcp-server
python -m build
# Erstellt: dist/figma_mcp-0.1.0-py3-none-any.whl
#           dist/figma_mcp-0.1.0.tar.gz
```

**c) Auf PyPI pushen**
```bash
# Test PyPI (empfohlen zuerst)
python -m twine upload --repository testpypi dist/*

# Produktiv PyPI
python -m twine upload dist/*
```

**d) Nach Upload installierbar mit:**
```bash
pip install figma-mcp
```

## 📊 Projekt-Status nach Push

Nach erfolgreichem Push ist dein Repository unter folgender URL erreichbar:

```
https://github.com/USERNAME/figma-mcp
```

**Was dann verfügbar ist:**
- ✅ Source Code
- ✅ Commits & History
- ✅ Issues Tracker
- ✅ Pull Requests
- ✅ README.md (auto-angezeigt)
- ✅ LICENSE (mit Badge)
- ✅ Releases (nach Tag-Push)
- ✅ CI/CD (mit Actions)

## 🎯 Mit Hermes verwenden

Nach dem Push können andere es installieren und verwenden:

```bash
# Installation
pip install figma-mcp

# Oder aus GitHub
pip install git+https://github.com/USERNAME/figma-mcp.git

# Mit Hermes
hermes mcp add figma --command python --args -m figma_mcp
hermes mcp test figma

# Nutzen
hermes ask "Liste meine Figma-Teams auf mit list_teams"
```

## 🔐 SSH-Authentifizierung (Optional)

Für SSH-basiertes Pushen:

```bash
# SSH Key generieren (falls nicht vorhanden)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Public Key zu GitHub hinzufügen
# https://github.com/settings/keys

# Remote auf SSH umstellen
git remote set-url origin git@github.com:USERNAME/figma-mcp.git

# Test
ssh -T git@github.com
# Hi USERNAME! You've successfully authenticated...
```

## 📚 Weitere Ressourcen

- [GitHub Help](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [PyPI Publishing](https://packaging.python.org/tutorials/packaging-projects/)
- [GitHub Actions](https://docs.github.com/en/actions)

## ✅ Checkliste

- [ ] GitHub Account erstellt
- [ ] Repository auf GitHub erstellt
- [ ] Local Repository mit remote verbunden
- [ ] Code gepusht (git push -u origin main)
- [ ] Auf https://github.com/USERNAME/figma-mcp sichtbar
- [ ] README.md wird angezeigt
- [ ] LICENSE vorhanden
- [ ] Topics hinzugefügt
- [ ] (Optional) Actions CI eingerichtet
- [ ] (Optional) Tags/Releases erstellt
- [ ] (Optional) Auf PyPI veröffentlicht

---

**Nächste Schritte:**
1. Repository erstellen
2. Code pushen
3. Mit anderen teilen
4. In Hermes verwenden
5. Feedback sammeln
6. Weitere Features hinzufügen

**Fragen?** Siehe GitHub Issues oder Discussions in deinem Repo!
