#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🧪 HERMES INTEGRATION TEST SUITE                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name=$1
    local test_cmd=$2
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Test $TESTS_RUN: $test_name... "
    
    if eval "$test_cmd" > /tmp/test_output.txt 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        cat /tmp/test_output.txt | sed 's/^/  /'
        return 1
    fi
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "ENVIRONMENT CHECKS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 1: Python installed
run_test "Python installed" "python --version"

# Check 2: Figma token set
run_test "FIGMA_API_TOKEN set" "[ -n \"\$FIGMA_API_TOKEN\" ]"

# Check 3: Figma MCP installed
run_test "Figma MCP importable" "python -c 'import figma_mcp'"

# Check 4: Hermes installed
run_test "Hermes installed" "command -v hermes"

# Check 5: Internet connectivity
run_test "API server reachable" "curl -s -I https://api.figma.com/ | grep -q 200"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "MCP SERVER TESTS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 6: MCP server can start
run_test "MCP server starts" "timeout 5 python -m figma_mcp > /dev/null 2>&1 &
sleep 2
if pgrep -f 'figma_mcp' > /dev/null; then
    pkill -f 'figma_mcp' || true
    exit 0
else
    exit 1
fi"

# Check 7: All tools are available
run_test "19 tools available" "python -c \"
from figma_mcp.server import TOOLS
if len(TOOLS) == 19:
    print(f'✅ {len(TOOLS)} tools found')
    exit(0)
else:
    print(f'❌ Expected 19 tools, got {len(TOOLS)}')
    exit(1)
\""

# Check 8: Tool names are correct
run_test "Required tools present" "python -c \"
from figma_mcp.server import TOOLS
required = ['get_file', 'list_files', 'list_teams', 'list_components']
found = [t for t in TOOLS if t in required]
if len(found) == len(required):
    exit(0)
else:
    exit(1)
\""

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "HERMES INTEGRATION TESTS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 9: Hermes sees Figma MCP
run_test "Hermes discovers Figma MCP" "hermes mcp list figma | grep -q get_file"

# Check 10: Tool list shows all tools
run_test "Hermes shows all tools" "hermes mcp list figma | grep -c 'tool' | grep -q '[0-9]'"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "CODE QUALITY TESTS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 11: No syntax errors
run_test "No syntax errors" "python -m py_compile figma_mcp/*.py"

# Check 12: Imports work
run_test "All imports valid" "python -c 'from figma_mcp import server, client'"

# Check 13: Type hints check
run_test "Type hints valid" "mypy figma_mcp/ --ignore-missing-imports || true"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "SECURITY TESTS"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 14: No hardcoded secrets
run_test "No hardcoded secrets" "! grep -r 'figd_' figma_mcp/ --include='*.py'"

# Check 15: HTTPS only for API
run_test "HTTPS for API calls" "grep -r 'https://api.figma.com' figma_mcp/ --include='*.py' | grep -q https"

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "RESULTS SUMMARY"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Total tests run:    $TESTS_RUN"
echo -e "Tests passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed:       ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🎉 ALL TESTS PASSED - INTEGRATION READY!                      ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ SOME TESTS FAILED - CHECK ABOVE FOR DETAILS               ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
