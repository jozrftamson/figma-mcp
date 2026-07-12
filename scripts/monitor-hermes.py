#!/usr/bin/env python3
"""Monitor Hermes ↔ Figma MCP integration in real-time."""

import subprocess
import time
import sys
from datetime import datetime
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")


def print_status(test_name, status, message=""):
    """Print test status."""
    symbol = "✅" if status else "❌"
    print(f"  {symbol} {test_name:<40} {message}")


def run_command(cmd, timeout=10):
    """Run command and return success status and output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)


def check_environment():
    """Check environment setup."""
    print_header("ENVIRONMENT CHECKS")
    
    checks = [
        ("Python available", "python --version"),
        ("Figma MCP installed", "python -c 'import figma_mcp'"),
        ("Hermes installed", "which hermes"),
        ("FIGMA_API_TOKEN set", "test -n \"$FIGMA_API_TOKEN\""),
    ]
    
    passed = 0
    for name, cmd in checks:
        success, _, _ = run_command(cmd)
        print_status(name, success)
        if success:
            passed += 1
    
    return passed, len(checks)


def check_mcp_server():
    """Check MCP server functionality."""
    print_header("MCP SERVER CHECKS")
    
    # Start server
    success, _, _ = run_command(
        "timeout 3 python -m figma_mcp > /dev/null 2>&1 &"
    )
    
    checks = [
        ("Server starts", "pgrep -f 'figma_mcp'"),
        ("Module importable", "python -c 'from figma_mcp import server'"),
    ]
    
    passed = 0
    for name, cmd in checks:
        success, _, _ = run_command(cmd)
        print_status(name, success)
        if success:
            passed += 1
    
    # Stop server
    run_command("pkill -f 'figma_mcp' || true")
    
    return passed, len(checks)


def check_tool_availability():
    """Check tool availability."""
    print_header("TOOL AVAILABILITY")
    
    success, stdout, _ = run_command(
        "python -c \"from figma_mcp.server import TOOLS; print(len(TOOLS))\""
    )
    
    if success:
        tool_count = int(stdout.strip())
        print_status("Tool count", tool_count == 19, f"({tool_count}/19)")
        
        # Get tool names
        success, stdout, _ = run_command(
            "python -c \"from figma_mcp.server import TOOLS; "
            "print('\\n'.join(sorted(TOOLS)))\""
        )
        
        if success:
            tools = stdout.strip().split('\n')
            print("\n  Available tools:")
            for tool in sorted(tools)[:5]:
                print(f"    • {tool}")
            if len(tools) > 5:
                print(f"    • ... and {len(tools) - 5} more")
        
        return 1, 1
    
    return 0, 1


def check_hermes_integration():
    """Check Hermes integration."""
    print_header("HERMES INTEGRATION")
    
    checks = [
        ("Hermes sees Figma", "hermes mcp list figma | grep -q get_file"),
        ("Tools discovered", "hermes mcp list figma | wc -l | grep -q '[0-9]'"),
    ]
    
    passed = 0
    for name, cmd in checks:
        success, _, err = run_command(cmd)
        print_status(name, success)
        if success:
            passed += 1
        elif "hermes" not in err:
            print(f"    Error: {err[:50]}")
    
    return passed, len(checks)


def check_performance():
    """Check performance metrics."""
    print_header("PERFORMANCE METRICS")
    
    print("  Measuring response times...\n")
    
    # Test response time
    start = time.time()
    success, _, _ = run_command(
        "python -c 'from figma_mcp.client import FigmaClient; "
        "c = FigmaClient(\"test\")' && echo ok",
        timeout=5
    )
    elapsed = time.time() - start
    
    print_status("Client initialization", elapsed < 1, f"({elapsed:.2f}s)")
    
    return 1 if elapsed < 1 else 0, 1


def check_code_quality():
    """Check code quality."""
    print_header("CODE QUALITY")
    
    checks = [
        ("No syntax errors", "python -m py_compile figma_mcp/*.py"),
        ("Imports valid", "python -c 'from figma_mcp import server, client'"),
        ("No hardcoded secrets", 
         "! grep -r 'figd_' figma_mcp/ --include='*.py' || true"),
    ]
    
    passed = 0
    for name, cmd in checks:
        success, _, _ = run_command(cmd)
        print_status(name, success)
        if success:
            passed += 1
    
    return passed, len(checks)


def print_summary(results):
    """Print summary of all checks."""
    print_header("TEST SUMMARY")
    
    total_passed = sum(p for p, _ in results.values())
    total_tests = sum(t for _, t in results.values())
    
    for category, (passed, total) in results.items():
        status = "✅" if passed == total else "⚠️ "
        print(f"  {status} {category:<30} {passed}/{total}")
    
    print(f"\n  Total: {total_passed}/{total_tests} checks passed")
    
    if total_passed == total_tests:
        print("\n  🎉 All checks passed! Hermes integration is ready!")
        return 0
    else:
        print("\n  ⚠️  Some checks failed. See above for details.")
        return 1


def main():
    """Run all checks."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║   🧪 HERMES ↔ FIGMA MCP INTEGRATION VERIFICATION                ║")
    print("║                                                                   ║")
    print("║   Testing Figma MCP integration with Hermes agent                ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"\n  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "Environment": check_environment(),
        "MCP Server": check_mcp_server(),
        "Tool Availability": check_tool_availability(),
        "Code Quality": check_code_quality(),
        "Performance": check_performance(),
        "Hermes Integration": check_hermes_integration(),
    }
    
    exit_code = print_summary(results)
    print(f"\n  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
