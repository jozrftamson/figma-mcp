#!/bin/bash

set -e

echo "🚀 Creating GitHub issue templates and automation..."

# Create issue templates
mkdir -p .github/ISSUE_TEMPLATE

# Bug Report
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: 'type/bug'
---

## 🐛 Bug Description
Clear and concise description of the bug.

## 📍 Reproduction Steps
1. Step one
2. Step two
3. Step three

## 🎯 Expected Behavior
What should happen?

## 😕 Actual Behavior
What actually happens?

## 📊 Environment
- **Python Version**: (e.g., 3.11)
- **OS**: (e.g., macOS, Ubuntu 22.04)
- **figma-mcp Version**: (e.g., 1.0.0)
- **Figma API Status**: Working / Not Working

## 📎 Attachments
Error logs, screenshots, etc.

## ✅ Checklist
- [ ] I've checked existing issues
- [ ] I've read the documentation
- [ ] The issue is reproducible
EOF

# Feature Request
cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature Request
about: Suggest an improvement or new feature
title: '[FEATURE] '
labels: 'type/feature'
---

## 🎯 Feature Description
Clear description of the requested feature.

## 🤔 Problem Statement
What problem does this solve?

## 💡 Proposed Solution
How should this be implemented?

## 🔄 Alternatives Considered
Any other approaches?

## 📚 Related Issues
- Closes #
- Related to #

## ✅ Checklist
- [ ] Feature aligns with project goals
- [ ] No existing issue for this
- [ ] Checked the roadmap
EOF

# Question/Discussion
cat > .github/ISSUE_TEMPLATE/question.md << 'EOF'
---
name: Question
about: Ask a question or start a discussion
title: '[QUESTION] '
labels: 'question'
---

## ❓ Question
What would you like to know?

## 📍 Context
Provide any relevant context or code examples.

## 🔍 Research
What have you already tried?

## 📚 Resources
Links to relevant documentation or issues.
EOF

echo "✅ Issue templates created!"

# Create GitHub Discussions template
mkdir -p .github/DISCUSSION_TEMPLATE

cat > .github/DISCUSSION_TEMPLATE/announcements.yml << 'EOF'
title: "Announcements"
labels: ["announcement"]
body:
  - type: markdown
    attributes:
      value: "# 📢 Project Announcement"
  - type: textarea
    attributes:
      label: "Announcement"
      description: "What's new?"
EOF

cat > .github/DISCUSSION_TEMPLATE/ideas.yml << 'EOF'
title: "Ideas & Suggestions"
labels: ["idea"]
body:
  - type: markdown
    attributes:
      value: "# 💡 Share Your Idea"
  - type: textarea
    attributes:
      label: "Idea"
      description: "What's your suggestion?"
EOF

echo "✅ Discussion templates created!"
