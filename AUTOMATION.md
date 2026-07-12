# 🤖 Figma MCP Server - Automation Setup Guide

Automatisiere Entwicklung, Testing, Deployment und Community Management.

## 📋 Table of Contents

1. [GitHub Actions CI/CD](#github-actions-cicd)
2. [Release Automation](#release-automation)
3. [Dependency Management](#dependency-management)
4. [Code Quality Automation](#code-quality-automation)
5. [Community Automation](#community-automation)
6. [Deployment Automation](#deployment-automation)
7. [Monitoring & Alerts](#monitoring--alerts)

---

## GitHub Actions CI/CD

### Workflow 1: Test & Build

**File:** `.github/workflows/ci.yml`

```yaml
name: CI - Tests & Build

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 2 * * *'  # Daily 2 AM

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with ruff
      run: ruff check figma_mcp/

    - name: Format check with black
      run: black --check figma_mcp/

    - name: Type check with mypy
      run: mypy figma_mcp/

    - name: Run tests with pytest
      run: pytest tests/ -v --cov=figma_mcp --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        fail_ci_if_error: false

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install build tools
      run: pip install build wheel

    - name: Build distribution
      run: python -m build

    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: python-package-distributions
        path: dist/
```

---

### Workflow 2: Security Scanning

**File:** `.github/workflows/security.yml`

```yaml
name: Security Scanning

on:
  push:
    branches: [ main, master ]
  pull_request:
  schedule:
    - cron: '0 3 * * 0'  # Weekly Sunday 3 AM

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -e ".[dev]"
        pip install bandit safety

    - name: Bandit security check
      run: bandit -r figma_mcp/ -f json -o bandit-report.json || true

    - name: Safety check (dependencies)
      run: safety check --json || true

    - name: OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        path: '.'
        format: 'JSON'
        args: >
          --enableExperimental
          --enableRetired

  codeql:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        language: ['python']

    steps:
    - uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: ${{ matrix.language }}

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
```

---

### Workflow 3: Docker Build & Push

**File:** `.github/workflows/docker.yml`

```yaml
name: Docker Build & Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Docker Hub
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Log in to GitHub Container Registry
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: |
          jozrftamson/figma-mcp
          ghcr.io/${{ github.repository }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=registry,ref=jozrftamson/figma-mcp:buildcache
        cache-to: type=registry,ref=jozrftamson/figma-mcp:buildcache,mode=max
```

---

## Release Automation

### Workflow 4: Automated Release

**File:** `.github/workflows/release.yml`

```yaml
name: Create Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Get version from tag
      id: tag_name
      run: |
        VERSION=${GITHUB_REF#refs/tags/v}
        echo "version=$VERSION" >> $GITHUB_OUTPUT

    - name: Generate changelog
      id: changelog
      run: |
        git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo 'HEAD')..HEAD > CHANGELOG_temp.md || true
        cat CHANGELOG_temp.md

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        body_path: CHANGELOG_temp.md
        draft: false
        prerelease: false
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## Dependency Management

### Workflow 5: Dependabot

**File:** `.github/dependabot.yml`

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "03:00"
    open-pull-requests-limit: 5
    allow:
      - dependency-type: all
    commit-message:
      prefix: "chore(deps):"
      include: "scope"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    commit-message:
      prefix: "ci:"
      include: "scope"
```

---

### Workflow 6: Dependency Updates Automation

**File:** `.github/workflows/dependencies.yml`

```yaml
name: Dependency Check & Update

on:
  schedule:
    - cron: '0 1 * * 0'  # Weekly Sunday 1 AM
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Check for outdated packages
      run: |
        pip install --upgrade pip
        pip list --outdated > outdated.txt
        cat outdated.txt

    - name: Create PR for updates
      if: hashFiles('outdated.txt') != ''
      uses: peter-evans/create-pull-request@v5
      with:
        commit-message: 'chore: update dependencies'
        title: 'chore: update dependencies'
        body: |
          ## Automated Dependency Update
          
          Outdated packages detected:
          
          $(cat outdated.txt)
        branch: chore/update-dependencies
        delete-branch: true
```

---

## Code Quality Automation

### Workflow 7: Code Quality Reports

**File:** `.github/workflows/quality.yml`

```yaml
name: Code Quality Analysis

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
        pip install pylint radon

    - name: Pylint check
      run: pylint figma_mcp/ --exit-zero --output-format=json > pylint.json || true

    - name: Code complexity (Radon)
      run: |
        radon cc figma_mcp/ -a > complexity.txt
        radon mi figma_mcp/ > maintainability.txt
        cat complexity.txt maintainability.txt

    - name: Coverage report
      run: |
        pytest tests/ --cov=figma_mcp --cov-report=term --cov-report=html:htmlcov
        
    - name: Upload coverage artifacts
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov/
```

---

## Community Automation

### Workflow 8: Issue & PR Management

**File:** `.github/workflows/community.yml`

```yaml
name: Community Management

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened, reopened]
  issue_comment:
    types: [created]

jobs:
  issue_response:
    if: github.event_name == 'issues' && github.event.action == 'opened'
    runs-on: ubuntu-latest
    steps:
    - name: Add welcome comment
      uses: actions/github-script@v6
      with:
        script: |
          const issue = context.issue;
          const body = `Thanks for opening this issue! 👋

We'll take a look and get back to you as soon as we can.

In the meantime:
- Read our [Contributing Guide](CONTRIBUTING.md)
- Check [similar issues](https://github.com/${{ github.repository }}/issues)
- See our [Roadmap](ROADMAP.md) for planned features

Feel free to ask if you have any questions!`;

          github.rest.issues.createComment({
            issue_number: issue.number,
            owner: issue.owner,
            repo: issue.repo,
            body: body
          });

  pr_response:
    if: github.event_name == 'pull_request' && github.event.action == 'opened'
    runs-on: ubuntu-latest
    steps:
    - name: Add PR welcome comment
      uses: actions/github-script@v6
      with:
        script: |
          const pr = context.payload.pull_request;
          const body = `Thanks for your contribution! 🎉

We'll review your PR shortly. Please make sure:
- ✅ Tests pass (\`pytest tests/ -v\`)
- ✅ Code is formatted (\`black figma_mcp/\`)
- ✅ Type checks pass (\`mypy figma_mcp/\`)
- ✅ Linting passes (\`ruff check figma_mcp/\`)

Need any help? Check [CONTRIBUTING.md](CONTRIBUTING.md)!`;

          github.rest.issues.createComment({
            issue_number: pr.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: body
          });

  add_labels:
    if: github.event_name == 'issues' && github.event.action == 'opened'
    runs-on: ubuntu-latest
    steps:
    - name: Auto-label issues
      uses: actions/github-script@v6
      with:
        script: |
          const title = context.payload.issue.title.toLowerCase();
          const labels = [];

          if (title.includes('bug') || title.includes('fix')) labels.push('bug');
          if (title.includes('feature') || title.includes('enhancement')) labels.push('enhancement');
          if (title.includes('doc')) labels.push('documentation');
          if (title.includes('question')) labels.push('question');

          if (labels.length > 0) {
            github.rest.issues.addLabels({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              labels: labels
            });
          }
```

---

## Deployment Automation

### Workflow 9: Deploy to Production

**File:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to Production

on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - 'figma_mcp/**'
      - 'pyproject.toml'
      - '.github/workflows/deploy.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://opencollective.com/figma-mcp
    steps:
    - uses: actions/checkout@v4

    - name: Deploy to PyPI
      run: |
        python -m pip install --upgrade pip
        pip install build twine
        python -m build
        python -m twine upload dist/* -u __token__ -p ${{ secrets.PYPI_TOKEN }}

    - name: Deploy Docker image
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: jozrftamson/figma-mcp:latest
        context: .

    - name: Update OpenCollective
      run: |
        echo "Deployment complete!"
        # Optional: webhook call to update stats
```

---

## Monitoring & Alerts

### Workflow 10: Health Checks

**File:** `.github/workflows/health.yml`

```yaml
name: Health Check

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Health check
      run: |
        pip install -e ".[dev]"
        pytest tests/ -v --tb=short

    - name: Create issue on failure
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          const issue = await github.rest.issues.create({
            owner: context.repo.owner,
            repo: context.repo.repo,
            title: '⚠️ Health check failed',
            body: 'Automated health check failed. Review: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}'
          });

    - name: Notify on Slack
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Health check failed for figma-mcp'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Local Development Automation

### Pre-commit Hook

**File:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
```

---

## Setup Automation Script

**File:** `scripts/setup-automation.sh`

```bash
#!/bin/bash

set -e

echo "🤖 Setting up automation for figma-mcp..."

# Create .github/workflows directory
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

echo "✅ Directories created"

# Install pre-commit
pip install pre-commit

# Setup pre-commit hooks
pre-commit install

echo "✅ Pre-commit hooks installed"

# Create GitHub Secrets reminder
cat > .github/SETUP_SECRETS.md << 'EOF'
# GitHub Secrets Setup

Add these secrets to your GitHub repository settings:

1. **PYPI_API_TOKEN** - PyPI API token for publishing
2. **DOCKERHUB_USERNAME** - Docker Hub username
3. **DOCKERHUB_TOKEN** - Docker Hub access token
4. **SLACK_WEBHOOK** - Slack webhook for notifications (optional)

Visit: Settings → Secrets and variables → Actions
EOF

echo "✅ Check .github/SETUP_SECRETS.md for required secrets"

echo "✅ Automation setup complete!"
```

---

## Task Automation (Makefile)

**File:** `Makefile`

```makefile
.PHONY: help setup test lint format build publish clean

help:
	@echo "figma-mcp - Development Tasks"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup          Setup development environment"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code"
	@echo "  type-check     Run type checking"
	@echo "  quality        Run full quality checks"
	@echo "  build          Build distribution"
	@echo "  publish        Publish to PyPI"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-push    Push Docker image"
	@echo "  clean          Clean build artifacts"

setup:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=figma_mcp --cov-report=html

lint:
	ruff check figma_mcp/
	black --check figma_mcp/

format:
	black figma_mcp/
	isort figma_mcp/

type-check:
	mypy figma_mcp/

quality: lint type-check test
	@echo "All quality checks passed!"

build:
	python -m build

publish: test quality build
	python -m twine upload dist/*

docker-build:
	docker build -t jozrftamson/figma-mcp:latest .

docker-push: docker-build
	docker push jozrftamson/figma-mcp:latest

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
```

---

## GitHub Labels

**File:** `.github/labels.json`

```json
[
  {
    "name": "type/bug",
    "color": "d73a4a",
    "description": "Something isn't working"
  },
  {
    "name": "type/feature",
    "color": "a2eeef",
    "description": "New feature or request"
  },
  {
    "name": "type/documentation",
    "color": "0075ca",
    "description": "Improvements or additions to documentation"
  },
  {
    "name": "priority/critical",
    "color": "ff0000",
    "description": "Must fix immediately"
  },
  {
    "name": "priority/high",
    "color": "ff6600",
    "description": "Should be fixed soon"
  },
  {
    "name": "good-first-issue",
    "color": "7057ff",
    "description": "Good for newcomers"
  },
  {
    "name": "help-wanted",
    "color": "008672",
    "description": "Extra attention is needed"
  },
  {
    "name": "status/in-progress",
    "color": "fbca04",
    "description": "Currently being worked on"
  },
  {
    "name": "status/blocked",
    "color": "fc2929",
    "description": "Blocked by another issue"
  }
]
```

---

## Automation Summary

This setup provides:

✅ **CI/CD Pipelines**
- Automated testing on multiple Python versions
- Code quality checks (lint, format, type hints)
- Security scanning
- Docker builds & pushes
- PyPI releases

✅ **Dependency Management**
- Dependabot for automatic updates
- Weekly dependency checks
- Automated PR creation

✅ **Community Management**
- Welcome comments on issues/PRs
- Auto-labeling
- Health checks
- Slack notifications

✅ **Developer Experience**
- Pre-commit hooks
- Makefile for common tasks
- Local automation setup

✅ **Production Deployment**
- Automated releases
- Docker registry pushes
- PyPI publishing

To enable:

1. Copy workflows to `.github/workflows/`
2. Add required GitHub secrets
3. Run `make setup` locally
4. Commit and push

---

**All automation is now set up for sustainable, scalable development!** 🚀

