#!/usr/bin/env python3
"""Interactive Code Review Checklist Tool."""

import os
import sys
from typing import List, Dict
from datetime import datetime


class ReviewChecklist:
    """Interactive code review checklist."""
    
    CATEGORIES = {
        "security": {
            "name": "🔒 Security",
            "items": [
                "No hardcoded secrets or credentials",
                "HTTPS used for external calls",
                "Input validation present",
                "SQL injection prevention (if applicable)",
                "Authentication/authorization implemented",
                "Rate limiting in place",
                "Data privacy respected",
                "Dependencies security checked"
            ]
        },
        "performance": {
            "name": "⚡ Performance",
            "items": [
                "No blocking operations in async code",
                "Connection pooling used",
                "N+1 queries avoided",
                "Caching implemented where needed",
                "Large objects freed properly",
                "API calls minimized",
                "Memory efficient",
                "Response time acceptable"
            ]
        },
        "testing": {
            "name": "🧪 Testing",
            "items": [
                "Unit tests written for new code",
                "Edge cases covered",
                "Error cases tested",
                "Integration tests present",
                "Test coverage maintained (>80%)",
                "Mocking used appropriately",
                "Tests pass locally",
                "No test interdependencies"
            ]
        },
        "quality": {
            "name": "✨ Code Quality",
            "items": [
                "PEP 8 style followed",
                "No linting errors",
                "Type hints present",
                "Functions not too large",
                "Cyclomatic complexity acceptable",
                "No magic numbers",
                "Naming is clear",
                "DRY principle followed"
            ]
        },
        "documentation": {
            "name": "📚 Documentation",
            "items": [
                "Functions have docstrings",
                "Complex logic explained",
                "README updated if needed",
                "CHANGELOG updated",
                "API changes documented",
                "Comments explain WHY not WHAT",
                "No commented-out code",
                "Examples provided"
            ]
        },
        "compatibility": {
            "name": "🔄 Compatibility",
            "items": [
                "Backwards compatible",
                "No breaking changes",
                "Works with supported Python versions",
                "Dependencies compatible",
                "Migration guide if needed",
                "Deprecation warnings added",
                "Tests pass on all versions",
                "No platform-specific issues"
            ]
        }
    }
    
    def __init__(self):
        self.results: Dict[str, Dict[str, any]] = {}
        self.start_time = datetime.now()
    
    def run_interactive_review(self) -> None:
        """Run interactive review session."""
        print("\n")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║           📋 FIGMA MCP - CODE REVIEW CHECKLIST             ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        for category_id, category_data in self.CATEGORIES.items():
            self._review_category(category_id, category_data)
        
        self._print_summary()
    
    def _review_category(self, category_id: str, category_data: Dict) -> None:
        """Review a category."""
        print(f"\n{category_data['name']}")
        print("=" * 60)
        
        passed = 0
        failed = 0
        skipped = 0
        
        for i, item in enumerate(category_data['items'], 1):
            while True:
                response = input(
                    f"  {i}. {item}? (y/n/s/quit): "
                ).lower().strip()
                
                if response == 'quit':
                    print("\nReview cancelled.")
                    sys.exit(0)
                elif response in ('y', 'yes'):
                    print("     ✅ PASS")
                    passed += 1
                    break
                elif response in ('n', 'no'):
                    # Ask for details
                    details = input("     ❌ FAIL - Details: ").strip()
                    print(f"     Logged: {details}")
                    failed += 1
                    break
                elif response in ('s', 'skip'):
                    print("     ⊘ SKIP")
                    skipped += 1
                    break
                else:
                    print("     Invalid input. Use y/n/s or quit.")
        
        self.results[category_id] = {
            "name": category_data['name'],
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total": len(category_data['items'])
        }
    
    def _print_summary(self) -> None:
        """Print review summary."""
        print("\n")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                    📊 REVIEW SUMMARY                       ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        
        for category_id, result in self.results.items():
            status = "✅" if result['failed'] == 0 else "❌"
            print(f"{status} {result['name']}")
            print(f"   Passed: {result['passed']}/{result['total']}")
            if result['failed'] > 0:
                print(f"   ❌ Failed: {result['failed']}")
            if result['skipped'] > 0:
                print(f"   ⊘ Skipped: {result['skipped']}")
            print()
            
            total_passed += result['passed']
            total_failed += result['failed']
            total_skipped += result['skipped']
        
        total_items = sum(len(cat['items']) for cat in self.CATEGORIES.values())
        success_rate = (total_passed / (total_items - total_skipped) * 100) if (total_items - total_skipped) > 0 else 0
        
        print("─" * 60)
        print(f"Total Items:  {total_items}")
        print(f"✅ Passed:    {total_passed}")
        print(f"❌ Failed:    {total_failed}")
        print(f"⊘ Skipped:    {total_skipped}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"Review Time: {int(elapsed // 60)}m {int(elapsed % 60)}s")
        print()
        
        if total_failed == 0:
            print("🎉 REVIEW PASSED - Ready to merge!")
        else:
            print("⚠️  REVIEW FAILED - Issues found above")
        
        print()


def main():
    """Main entry point."""
    checklist = ReviewChecklist()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick mode - just print categories
        for cat_id, cat_data in checklist.CATEGORIES.items():
            print(f"\n{cat_data['name']}")
            for item in cat_data['items']:
                print(f"  - [ ] {item}")
    else:
        # Interactive mode
        checklist.run_interactive_review()


if __name__ == "__main__":
    main()
