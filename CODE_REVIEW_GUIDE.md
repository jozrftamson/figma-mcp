# 📋 Code Review System für Figma MCP Server

Automatisiertes Code Review System mit Standards, Checklisten und Automatisierung.

---

## 📑 Table of Contents

1. [Code Review Standards](#code-review-standards)
2. [Review Checklisten](#review-checklisten)
3. [Automatisierte Checks](#automatisierte-checks)
4. [Review Workflow](#review-workflow)
5. [GitHub Automation](#github-automation)
6. [Best Practices](#best-practices)

---

## Code Review Standards

### Review Prinzipien

```
1. RESPECTFUL & CONSTRUCTIVE
   ✓ Kritik auf Code, nicht Person
   ✓ Lösungsvorschläge anbieten
   ✓ Positive Aspekte würdigen

2. THOROUGH BUT EFFICIENT
   ✓ Alle kritischen Areas prüfen
   ✓ Nicht zu lange Reviews
   ✓ Fokus auf wichtige Probleme

3. CONSISTENT
   ✓ Standards befolgen
   ✓ Gleiche Anforderungen für alle
   ✓ Dokumentierte Richtlinien

4. KNOWLEDGE SHARING
   ✓ Lernen ermöglichen
   ✓ Best Practices weitergeben
   ✓ Team-Wissenstransfer
```

### Code Quality Standards

```python
# ✅ GOOD: Type hints, error handling, documentation
async def get_file(
    self,
    file_key: str,
    version_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve a Figma file.
    
    Args:
        file_key: The file key
        version_id: Optional version ID
        
    Returns:
        File data dictionary
        
    Raises:
        FileNotFoundError: If file not found
        PermissionError: If no access
    """
    if not file_key:
        raise ValueError("file_key required")
    
    try:
        endpoint = f"/files/{file_key}"
        return await self._request("GET", endpoint)
    except httpx.HTTPError as e:
        logger.error(f"Failed to get file: {e}")
        raise


# ❌ BAD: No type hints, no error handling, no docs
async def get_file(self, key, version=None):
    endpoint = f"/files/{key}"
    return await self._request("GET", endpoint)
```

### Style Guide

```python
# IMPORTS (organized in 3 groups)
import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel

from figma_mcp import constants


# TYPE HINTS (always required)
def function(name: str, count: int = 10) -> List[str]:
    pass


# NAMING (PEP 8 conventions)
CONSTANT_VALUE = 100
class MyClass:
    def method_name(self) -> None:
        local_variable = "value"


# LINE LENGTH (max 88 characters with black)
# ✅ Good
result = some_function(
    arg1="value",
    arg2="another",
    arg3="value"
)

# ❌ Bad
result = some_function(arg1="value", arg2="another", arg3="value", arg4="extra")


# COMMENTS (only when necessary)
# ✅ Good: Explains WHY
# Retry on rate limiting (Figma API: 120 req/min)
if response.status == 429:
    await asyncio.sleep(10)

# ❌ Bad: Explains WHAT (obvious from code)
# Increment counter
count += 1


# ERROR HANDLING (always specific)
# ✅ Good
try:
    data = await self._request("GET", endpoint)
except httpx.TimeoutException:
    logger.warning("Timeout, retrying...")
except httpx.HTTPError as e:
    logger.error(f"API error: {e}")
    raise

# ❌ Bad
try:
    data = await self._request("GET", endpoint)
except:
    pass
```

---

## Review Checklisten

### Security Checklist

```markdown
## 🔒 Security Review

- [ ] **No hardcoded secrets**
  - [ ] API tokens not in code
  - [ ] Passwords not in comments
  - [ ] Configuration files checked

- [ ] **No SQL Injection** (if applicable)
  - [ ] Input validation present
  - [ ] Parameterized queries used
  
- [ ] **HTTPS only**
  - [ ] All external calls HTTPS
  - [ ] No HTTP fallback
  
- [ ] **Authentication/Authorization**
  - [ ] Token validation present
  - [ ] Permissions checked
  - [ ] Rate limiting implemented
  
- [ ] **Data Privacy**
  - [ ] Sensitive data not logged
  - [ ] PII handled securely
  - [ ] Data sanitization done
  
- [ ] **Dependency security**
  - [ ] Dependencies up-to-date
  - [ ] Known vulnerabilities checked
  - [ ] Pinned versions where needed
```

### Performance Checklist

```markdown
## ⚡ Performance Review

- [ ] **Async/Await optimization**
  - [ ] No blocking calls in async
  - [ ] Parallel operations where possible
  - [ ] Connection pooling used
  
- [ ] **Memory efficiency**
  - [ ] No memory leaks
  - [ ] Large objects freed
  - [ ] Generators used for streams
  
- [ ] **API calls optimized**
  - [ ] Minimal requests
  - [ ] Caching implemented
  - [ ] Batch operations used
  
- [ ] **Database queries**
  - [ ] N+1 problems avoided
  - [ ] Indexes used
  - [ ] Query optimization done
  
- [ ] **Code efficiency**
  - [ ] No unnecessary loops
  - [ ] Algorithms optimal
  - [ ] Time complexity acceptable
  
- [ ] **Network**
  - [ ] Compression enabled
  - [ ] Connection reuse
  - [ ] Timeout values appropriate
```

### Testing Checklist

```markdown
## 🧪 Testing Review

- [ ] **Unit Tests**
  - [ ] New code has tests
  - [ ] Edge cases covered
  - [ ] Coverage maintained (>80%)
  
- [ ] **Integration Tests**
  - [ ] API calls mocked
  - [ ] Error cases tested
  - [ ] Workflows tested
  
- [ ] **Test Quality**
  - [ ] Tests are isolated
  - [ ] No test interdependencies
  - [ ] Clear test names
  - [ ] Documentation present
  
- [ ] **Error Handling**
  - [ ] Exception testing
  - [ ] Error messages useful
  - [ ] Logging adequate
  
- [ ] **Test Coverage**
  - [ ] Happy path covered
  - [ ] Error paths covered
  - [ ] Edge cases covered
```

### Documentation Checklist

```markdown
## 📚 Documentation Review

- [ ] **Code Documentation**
  - [ ] Functions have docstrings
  - [ ] Complex logic explained
  - [ ] Type hints present
  
- [ ] **Comments**
  - [ ] Why, not what
  - [ ] Accurate and up-to-date
  - [ ] No commented code
  
- [ ] **Changelog**
  - [ ] CHANGELOG.md updated
  - [ ] Breaking changes noted
  - [ ] Features documented
  
- [ ] **README**
  - [ ] Setup instructions clear
  - [ ] Examples provided
  - [ ] Links working
  
- [ ] **API Documentation**
  - [ ] Parameters documented
  - [ ] Return types clear
  - [ ] Exceptions documented
```

### Code Quality Checklist

```markdown
## ✨ Code Quality Review

- [ ] **Style Compliance**
  - [ ] PEP 8 followed
  - [ ] Formatting consistent
  - [ ] No linting errors
  
- [ ] **Type Safety**
  - [ ] Type hints complete
  - [ ] MyPy passing
  - [ ] No type: ignore without reason
  
- [ ] **Complexity**
  - [ ] Functions not too large
  - [ ] Cyclomatic complexity low
  - [ ] Nesting levels reasonable
  
- [ ] **Maintainability**
  - [ ] Code is DRY
  - [ ] Naming is clear
  - [ ] No magic numbers
  
- [ ] **Error Handling**
  - [ ] Specific exceptions
  - [ ] Graceful degradation
  - [ ] Error recovery
  
- [ ] **Naming**
  - [ ] Variables meaningful
  - [ ] Functions descriptive
  - [ ] Classes clear
```

---

## Automatisierte Checks

### GitHub Actions Workflow

**File:** `.github/workflows/code-review.yml`

```yaml
name: Automated Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
        pip install pylint radon

    - name: Lint check
      run: ruff check figma_mcp/ --output-format=github
      continue-on-error: true

    - name: Format check
      run: black --check figma_mcp/
      continue-on-error: true

    - name: Type check
      run: mypy figma_mcp/ --ignore-missing-imports
      continue-on-error: true

    - name: Security check
      run: |
        bandit -r figma_mcp/ -f json -o bandit-report.json
        cat bandit-report.json | python -m json.tool
      continue-on-error: true

    - name: Complexity analysis
      run: |
        radon cc figma_mcp/ -a
        radon mi figma_mcp/ -s
      continue-on-error: true

    - name: Comment with review results
      uses: actions/github-script@v6
      if: always()
      with:
        script: |
          const fs = require('fs');
          const banditReport = JSON.parse(fs.readFileSync('bandit-report.json', 'utf8'));
          
          let comment = '## 📋 Automated Code Review\n\n';
          
          if (banditReport.results.length > 0) {
            comment += '### 🔒 Security Issues Found\n';
            banditReport.results.forEach(issue => {
              comment += `- **${issue.test_id}**: ${issue.issue_text}\n`;
            });
          } else {
            comment += '### ✅ Security: No issues found\n';
          }
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

### Pre-commit Hooks für Review

**File:** `.pre-commit-config.yaml`

```yaml
repos:
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
        additional_dependencies: [types-requests]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, figma_mcp/]
```

---

## Review Workflow

### Step-by-Step Process

```
1. DEVELOPER: Push Feature Branch
   git checkout -b feature/my-feature
   # ... make changes ...
   git push origin feature/my-feature

2. DEVELOPER: Create Pull Request
   • Use PR template
   • Fill all sections
   • Link related issues
   • Set reviewers

3. AUTOMATED: Run CI/CD
   ✓ Tests run
   ✓ Linting checks
   ✓ Security scan
   ✓ Build verification

4. REVIEWER: Check Automated Feedback
   • Review CI/CD results
   • Check code quality metrics
   • Assess security scan

5. REVIEWER: Manual Code Review
   • Security check
   • Performance check
   • Testing check
   • Documentation check
   • Code quality check

6. REVIEWER: Leave Comments
   • Suggestions with context
   • Questions for clarification
   • References to standards
   • Actionable feedback

7. DEVELOPER: Address Feedback
   • Make changes
   • Respond to comments
   • Request re-review
   • Mark as resolved

8. REVIEWER: Approve or Request Changes
   • Check all feedback addressed
   • Verify fixes appropriate
   • Approve PR

9. MAINTAINER: Merge
   • Squash commits if needed
   • Merge to main
   • Delete feature branch

10. AUTOMATION: Post-merge Actions
    • Close related issues
    • Update changelog
    • Trigger deployment
```

### PR Template

**File:** `.github/pull_request_template.md`

```markdown
## Description
Brief description of changes.

## Related Issues
Closes #123

## Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 🔄 Refactoring
- [ ] 📚 Documentation
- [ ] ⚡ Performance
- [ ] 🔒 Security

## How Has This Been Tested?
Describe testing approach:
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings
- [ ] Backwards compatible
- [ ] Security reviewed

## Screenshots (if applicable)
Add screenshots for UI changes.

## Additional Notes
Any additional information reviewers should know.
```

---

## GitHub Automation

### Auto-Request Reviewers

```yaml
name: Auto-Assign Reviewers

on:
  pull_request:
    types: [opened]

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/github-script@v6
      with:
        script: |
          const reviewers = ['user1', 'user2', 'user3'];
          const selectedReviewers = reviewers
            .sort(() => 0.5 - Math.random())
            .slice(0, 2);
          
          github.rest.pulls.requestReviewers({
            owner: context.repo.owner,
            repo: context.repo.repo,
            pull_number: context.issue.number,
            reviewers: selectedReviewers
          });
```

### Review Size Warning

```yaml
name: PR Size Check

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  size:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/github-script@v6
      with:
        script: |
          const pr = context.payload.pull_request;
          const additions = pr.additions;
          const deletions = pr.deletions;
          const changes = additions + deletions;
          
          let comment = '## PR Size Analysis\n\n';
          comment += `- **Changes**: +${additions} -${deletions}\n`;
          comment += `- **Total**: ${changes} lines\n\n`;
          
          if (changes > 500) {
            comment += '⚠️ This PR is quite large. Consider breaking it into smaller PRs.\n';
          } else if (changes > 200) {
            comment += 'ℹ️ This is a medium-sized PR.\n';
          } else {
            comment += '✅ This is a nice, reviewable size.\n';
          }
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

---

## Best Practices

### For Reviewers

```markdown
1. TIMING
   ✓ Review within 24 hours
   ✓ Don't let PRs linger
   ✓ Be responsive to updates

2. COMMUNICATION
   ✓ Be specific and clear
   ✓ Reference documentation
   ✓ Ask questions, don't assume
   ✓ Acknowledge good code

3. BALANCE
   ✓ Pick battles carefully
   ✓ Standard > Perfection
   ✓ Allow different styles
   ✓ Focus on important issues

4. LEARNING
   ✓ Teach why, not just what
   ✓ Share resources
   ✓ Ask for explanations
   ✓ Review as learning opportunity

5. TRUST
   ✓ Assume good intent
   ✓ Trust domain expertise
   ✓ Suggest, not demand
   ✓ Build team culture

GOOD REVIEW COMMENT:
"This approach works, but I'm concerned about performance
with large file lists. Have you considered using pagination?
See: [link]. Could you add a test for this?"

BAD REVIEW COMMENT:
"This is wrong. Fix it."
```

### For Developers

```markdown
1. SELF REVIEW FIRST
   ✓ Read your own code first
   ✓ Fix obvious issues
   ✓ Check against standards
   ✓ Run all checks locally

2. CLEAR PR DESCRIPTION
   ✓ Explain what, why, how
   ✓ Link related issues
   ✓ Describe testing
   ✓ Note any concerns

3. RESPOND TO FEEDBACK
   ✓ Reply to all comments
   ✓ Explain your reasoning
   ✓ Make changes or discuss
   ✓ Update PR accordingly

4. REQUEST RE-REVIEW
   ✓ After making changes
   ✓ Clear what was changed
   ✓ Link to new commits
   ✓ Ask specific questions

5. LEARN FROM FEEDBACK
   ✓ Understand the reasoning
   ✓ Apply to future PRs
   ✓ Ask if unclear
   ✓ Thank reviewers
```

---

## Review Metrics

Track to improve process:

```python
# Average review time
total_time = sum(pr.merged_at - pr.created_at for pr in merged_prs)
average_review_time = total_time / len(merged_prs)

# Review comments per PR
average_comments = sum(pr.comment_count for pr in merged_prs) / len(merged_prs)

# Reviewer participation
reviewer_counts = {}
for pr in merged_prs:
    for reviewer in pr.reviewers:
        reviewer_counts[reviewer] = reviewer_counts.get(reviewer, 0) + 1

# Revision requests
revision_requests = sum(1 for pr in merged_prs if pr.revision_requested)

# Approval rate
approvals = sum(1 for pr in merged_prs if pr.approved)
approval_rate = approvals / len(merged_prs) * 100
```

---

## Summary

Ein strukturiertes Code Review System mit:
- ✅ Klaren Standards
- ✅ Automatisierten Checks
- ✅ Hilfreichen Checklisten
- ✅ GitHub Automation
- ✅ Best Practices
- ✅ Messbare Metriken

**Ziel:** Hohe Codequalität + positive Team-Kultur! 🎯

