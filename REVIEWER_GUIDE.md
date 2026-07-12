# 👥 Reviewer Guide - Figma MCP Code Reviews

Praktischer Guide für Code Reviewer im Figma MCP Projekt.

---

## 🎯 Deine Rolle als Reviewer

```
RESPONSIBILITY:
  ✓ Ensure code quality
  ✓ Catch potential bugs
  ✓ Share knowledge
  ✓ Maintain standards
  ✓ Support developers
  
AUTHORITY:
  ✓ Request changes
  ✓ Request clarification
  ✓ Suggest improvements
  ✓ Approve for merge
  
NOT YOUR JOB:
  ✗ Rewrite code (suggest changes instead)
  ✗ Be mean or dismissive
  ✗ Block PRs indefinitely
  ✗ Review without understanding
```

---

## 📋 Review Process

### Before You Start

```
1. UNDERSTAND THE CONTEXT
   - Read PR description
   - Check related issues
   - Understand goal
   - Know acceptance criteria

2. CHECK AUTOMATED RESULTS
   - All CI/CD passing?
   - All tests passing?
   - No security issues?
   - Code quality OK?

3. PLAN YOUR REVIEW
   - Files affected?
   - Complexity level?
   - Time available?
   - Special attention areas?
```

### During Review

```
1. READ THE CODE
   - Top-to-bottom once
   - Understand flow
   - Check for bugs
   - Note areas for deeper review

2. DETAILED ANALYSIS
   - Check each file carefully
   - Look for patterns
   - Review against standards
   - Check for edge cases

3. RUN LOCALLY (Optional)
   - Check it actually works
   - Manual testing
   - Performance check
   - Edge case testing

4. GATHER FEEDBACK
   - Issues found
   - Suggestions
   - Questions
   - Compliments
```

### Writing Comments

```
GOOD COMMENT STRUCTURE:

1. Observation (WHAT)
   "I notice the error handling here doesn't check for timeout exceptions."

2. Impact (WHY)
   "This could cause the app to crash if the Figma API is slow."

3. Suggestion (HOW)
   "Consider catching httpx.TimeoutException separately:
   try:
       response = await self._request(...)
   except httpx.TimeoutException:
       logger.warning('API timeout, retrying...')
       await asyncio.sleep(2)
   except httpx.HTTPError as e:
       raise"

4. Reference (WHERE)
   "See: https://docs.python-httpx.org/exceptions.html"

5. Tone (HOW FRIENDLY)
   "This would make the code more robust. What do you think?"
```

---

## 💬 Comment Guidelines

### Good Comments

```markdown
✅ "This looks good, but I'm concerned about the performance
    with large file lists. Have you considered pagination?
    See the Figma API docs: [link]. Could you add a test for this?"

✅ "Great implementation! I noticed the error handling could be
    more specific. Instead of catching all exceptions, consider:
    [code example]"

✅ "I don't understand this logic. Could you add a comment
    explaining why we need to retry here?"

✅ "I like how you structured this! It's much more maintainable
    than the previous approach."

✅ "I think there might be a race condition here. What if
    two requests try to access this at the same time?"
```

### Bad Comments

```markdown
❌ "This is wrong."
❌ "Why would you do it this way?"
❌ "This code is terrible."
❌ "Just fix it."
❌ "I don't like this."
```

### Tone Tips

```
REPLACE:           WITH:
"You should..."     "Would it be better to...?"
"Wrong approach"    "I think there's a better way..."
"This is bad"       "This might cause issues because..."
"Fix this"          "Could you fix this? Here's why..."
"Obviously..."      "I might be missing something, but..."
```

---

## 🔍 What to Look For

### Security Issues (HIGH PRIORITY)

```python
# ❌ BAD: Hardcoded token
API_TOKEN = "figd_abc123"

# ❌ BAD: No HTTPS
response = requests.get("http://api.figma.com/...")

# ❌ BAD: No input validation
def get_file(file_id):
    return fetch(f"/files/{file_id}")

# ❌ BAD: Generic exception handling
try:
    data = fetch_data()
except:
    pass

# ✅ GOOD: All above issues fixed
API_TOKEN = os.getenv("FIGMA_API_TOKEN")
response = httpx.get("https://api.figma.com/...")
if not file_id or not isinstance(file_id, str):
    raise ValueError("Invalid file_id")
try:
    data = fetch_data()
except httpx.TimeoutException:
    logger.warning("Timeout")
    raise
```

### Performance Issues (MEDIUM PRIORITY)

```python
# ❌ BAD: N+1 problem
for team in teams:
    projects = fetch(f"/teams/{team.id}/projects")

# ❌ BAD: Blocking in async
async def get_data():
    time.sleep(1)  # BLOCKS!

# ❌ BAD: No connection reuse
for i in range(100):
    client = httpx.AsyncClient()
    await client.get("...")

# ✅ GOOD: Batch operations
projects = fetch_all_projects(team_ids)

# ✅ GOOD: Async all the way
async def get_data():
    await asyncio.sleep(1)

# ✅ GOOD: Reuse client
async with httpx.AsyncClient() as client:
    for i in range(100):
        await client.get("...")
```

### Testing Issues (MEDIUM PRIORITY)

```python
# ❌ BAD: No tests
def new_feature():
    pass

# ❌ BAD: Incomplete tests
def test_new_feature():
    result = new_feature()
    assert result is not None

# ❌ BAD: Test depends on others
def test_a():
    setup_data()

def test_b():  # Depends on test_a running first!
    data = get_data()

# ✅ GOOD: Tests with edge cases
def test_new_feature():
    # Happy path
    result = new_feature("valid")
    assert result["success"]
    
    # Error case
    with pytest.raises(ValueError):
        new_feature("")
    
    # Edge case
    result = new_feature("x" * 1000)
    assert result["success"]

# ✅ GOOD: Tests are independent
def test_get_file_success(mock_client):
    mock_client.return_value = {"name": "file"}
    result = get_file("123")
    assert result["name"] == "file"
```

### Documentation Issues (LOW PRIORITY)

```python
# ❌ BAD: No documentation
async def get_file(file_key, version_id):
    ...

# ❌ BAD: Obvious comment
# Increment counter
count += 1

# ✅ GOOD: Clear documentation
async def get_file(
    file_key: str,
    version_id: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve a Figma file.
    
    Args:
        file_key: The file key (required)
        version_id: Optional version ID
        
    Returns:
        Dictionary with file data
        
    Raises:
        FileNotFoundError: If file not found
        PermissionError: If no access
    """

# ✅ GOOD: Explains WHY
# Retry on rate limiting per Figma API docs
if response.status == 429:
    await asyncio.sleep(60)
```

---

## 🎓 Teaching While Reviewing

```
GOAL: Help developer learn, not just fix code

APPROACH:
1. Ask questions first
   "What's the reason for this approach?"
   
2. Provide context
   "In async code, we should avoid blocking calls
    because... Here's a resource: [link]"
   
3. Offer alternatives
   "Option A: [your code]
    Option B: [alternative]
    I prefer Option A because..."
   
4. Share resources
   "This is a common pattern. See:
    - [Article]
    - [Documentation]
    - [Example code]"

5. Acknowledge good code
   "Great use of async/await here!"
   "I like how you structured this!"
```

---

## ⏱️ Review Speed Guidelines

```
SMALL PR (1-100 lines)
  → 15-30 minutes
  
MEDIUM PR (100-300 lines)
  → 30-60 minutes
  
LARGE PR (300+ lines)
  → 1-2 hours or request smaller PR
  
HUGE PR (500+ lines)
  → Request split into smaller PRs
```

### When to Request Changes

```
Always request changes for:
  ✗ Security issues
  ✗ Breaking changes not documented
  ✗ Missing tests for new features
  ✗ Code that doesn't follow standards

Suggest as improvement for:
  ? Performance concerns
  ? Code style preferences
  ? Better approaches
  ? Missing documentation

Comment for learning:
  ℹ Good patterns you want to highlight
  ℹ Resource recommendations
  ℹ Future improvements
```

---

## 👍 Approval Criteria

Approve only when:

```
✅ Code quality is good
✅ All tests pass
✅ Security is OK
✅ Documentation updated
✅ No blockers remaining
✅ Developer addressed concerns
✅ Performance is acceptable
✅ Backwards compatible (if needed)
```

---

## 📊 Feedback Template

```markdown
## Code Review Summary

**Overall**: [APPROVED / CHANGES REQUESTED / COMMENT]

### Security ✅/⚠️
[Details]

### Performance ✅/⚠️
[Details]

### Testing ✅/⚠️
[Details]

### Code Quality ✅/⚠️
[Details]

### Documentation ✅/⚠️
[Details]

### Questions
[Questions for developer]

### Great Job On
[Compliments]

### Next Steps
[What developer should do]
```

---

## 🚀 Quick Review Checklist

```
Before approving:

SECURITY (30 sec)
  ☐ No hardcoded secrets
  ☐ HTTPS/secure calls
  ☐ Input validation

TESTS (30 sec)
  ☐ Tests added for new code
  ☐ Edge cases covered
  ☐ All pass

QUALITY (1 min)
  ☐ Follows standards
  ☐ Type hints present
  ☐ Readable code

DOCS (30 sec)
  ☐ README updated
  ☐ Docstrings present
  ☐ CHANGELOG updated

PERFORMANCE (1 min)
  ☐ No obvious inefficiencies
  ☐ Appropriate algorithms
  ☐ No N+1 problems

TOTAL TIME: ~4 minutes for standard PR
```

---

## 🎯 Performance Tips for Reviewers

```
1. USE TOOLS
   - GitHub's file comments
   - Batch feedback vs one-by-one
   - Use templates

2. EFFICIENT READING
   - Skim code first
   - Focus on logic, not formatting (tools catch that)
   - Trust automated checks

3. SMART QUESTIONS
   - Ask why, not just what
   - Single comprehensive comment vs many small

4. MOVE FAST
   - Don't overthink
   - Use standard checklists
   - Suggest but don't demand perfection

5. ESCALATE IF NEEDED
   - Complex areas → ask team lead
   - Big debates → discuss offline
   - Disagreements → get second opinion
```

---

## 💪 Reviewer Skills

### Develop These

```
TECHNICAL SKILLS:
  → Understanding the codebase
  → Pattern recognition
  → Security awareness
  → Performance knowledge

COMMUNICATION SKILLS:
  → Clear explanations
  → Constructive feedback
  → Asking good questions
  → Teaching ability

SOFT SKILLS:
  → Empathy
  → Patience
  → Growth mindset
  → Humility
```

### Resources to Learn More

```
- "Code Review Best Practices" [Google]
- "Respectful Code Review" [Medium]
- "The Art of Code Review" [InfoQ]
- Python security: [OWASP]
- Async patterns: [Real Python]
```

---

## 🤝 Team Culture

```
REMEMBER:
  ✓ Every developer wants to write good code
  ✓ Reviews are learning opportunities
  ✓ Be the reviewer you want
  ✓ Praise good code publicly
  ✓ Fix issues privately if possible
  ✓ Assume good intent
  ✓ Learn from different approaches
```

---

**You're not just catching bugs.  
You're building a culture of excellence!** 🌟

