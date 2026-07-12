#!/bin/bash

set -e

echo "🤖 Setting up automation for figma-mcp..."

# Check if git is initialized
if [ ! -d .git ]; then
    echo "⚠️  Not in a git repository. Please run this from the project root."
    exit 1
fi

# Create .github/workflows directory
echo "📁 Creating directories..."
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

# Install pre-commit if not already installed
echo "🔧 Installing pre-commit..."
pip install pre-commit --quiet

# Setup pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install
pre-commit install --hook-type pre-push

# Create GitHub Secrets reminder
echo "📝 Creating secrets reminder..."
cat > .github/SETUP_SECRETS.md << 'EOF'
# GitHub Secrets Setup

Add these secrets to your GitHub repository settings:

## Required Secrets

1. **DOCKERHUB_USERNAME** - Docker Hub username
   - Get at: https://hub.docker.com/settings/security
   
2. **DOCKERHUB_TOKEN** - Docker Hub access token
   - Create at: https://hub.docker.com/settings/security

3. **PYPI_API_TOKEN** - PyPI API token (for automatic releases)
   - Create at: https://pypi.org/manage/account/

## Optional Secrets

- **SLACK_WEBHOOK** - Slack webhook for notifications
- **GITHUB_TOKEN** - Usually auto-provided by GitHub

## Setup Instructions

1. Go to: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret above

## Running Workflows Locally

To test workflows locally, install act:

```bash
# macOS
brew install act

# Ubuntu/Debian
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run a workflow
act -j test
```

Visit https://github.com/nektos/act for more info.
EOF

# Create label setup script
echo "🏷️  Creating label setup script..."
cat > scripts/setup-labels.sh << 'EOF'
#!/bin/bash

# Add GitHub labels
# Requires gh CLI: https://cli.github.com/

labels=(
    "type/bug:d73a4a:Something isn't working"
    "type/feature:a2eeef:New feature or request"
    "type/documentation:0075ca:Improvements or additions to documentation"
    "type/refactor:fbca04:Code refactoring"
    "priority/critical:ff0000:Must fix immediately"
    "priority/high:ff6600:Should be fixed soon"
    "priority/medium:fbca04:Normal priority"
    "priority/low:0075ca:Low priority"
    "good-first-issue:7057ff:Good for newcomers"
    "help-wanted:008672:Extra attention is needed"
    "status/in-progress:fbca04:Currently being worked on"
    "status/blocked:fc2929:Blocked by another issue"
    "status/on-hold:cccccc:On hold"
)

echo "🏷️  Setting up GitHub labels..."
for label in "${labels[@]}"; do
    IFS=':' read -r name color desc <<< "$label"
    gh label create "$name" -c "$color" -d "$desc" 2>/dev/null || true
done
echo "✅ Labels setup complete!"
EOF

chmod +x scripts/setup-labels.sh

# Create a contribution template
echo "📄 Creating additional templates..."
cat > .github/ISSUE_TEMPLATE/performance.md << 'EOF'
---
name: Performance Issue
about: Report a performance problem
---

## Performance Issue

### Description
What is the performance problem?

### Current Performance
How long does it take?

### Expected Performance
What should it be?

### Steps to Reproduce
1.
2.
3.

### Environment
- Python version: 
- OS: 
- figma-mcp version: 

### Additional context
EOF

# Git add automation files
echo "📦 Committing automation setup..."
git add .github/ .pre-commit-config.yaml Makefile scripts/ 2>/dev/null || true

echo ""
echo "✅ Automation setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add secrets: Settings → Secrets and variables → Actions"
echo "   See: .github/SETUP_SECRETS.md"
echo ""
echo "2. (Optional) Setup GitHub labels:"
echo "   gh auth login"
echo "   bash scripts/setup-labels.sh"
echo ""
echo "3. Test workflows locally (requires 'act'):"
echo "   act -j test"
echo ""
echo "4. Use Makefile for development:"
echo "   make help"
echo ""
echo "📚 Documentation: See AUTOMATION.md"
echo ""
