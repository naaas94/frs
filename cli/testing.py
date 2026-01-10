"""
Auto-Test Framework

Runs pytest on solutions and reports results.

Usage:
    python -m cli.testing hashmap/problem_01_group_anagrams
    python -m cli.testing --all
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


@dataclass
class TestResult:
    """Result of running tests on a problem."""
    problem: str
    passed: int
    failed: int
    errors: int
    total: int
    duration: float
    output: str
    failed_tests: List[Dict]


class TestRunner:
    """Runs tests and formats results."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.base_dir = Path(__file__).parent.parent
        self.problems_dir = self.base_dir / "problems"
        self.solutions_dir = self.base_dir / "solutions"
    
    def find_test_file(self, problem_path: str) -> Optional[Path]:
        """Find the test file for a problem."""
        problem_dir = self.problems_dir / problem_path
        
        # Look for test file
        for pattern in ["test_*.py", "tests.py", "*_test.py"]:
            matches = list(problem_dir.glob(pattern))
            if matches:
                return matches[0]
        
        return None
    
    def find_solution_file(self, problem_path: str) -> Optional[Path]:
        """Find the user's solution file."""
        # Check solutions directory first
        solution_file = self.solutions_dir / problem_path / "solution.py"
        if solution_file.exists():
            return solution_file
        
        # Check problem directory for solution_template.py
        template = self.problems_dir / problem_path / "solution_template.py"
        if template.exists():
            return template
        
        return None
    
    def run_tests(self, problem_path: str, timeout: int = 30) -> TestResult:
        """Run tests for a specific problem."""
        test_file = self.find_test_file(problem_path)
        
        if not test_file:
            return TestResult(
                problem=problem_path,
                passed=0, failed=0, errors=1, total=0,
                duration=0.0,
                output="No test file found",
                failed_tests=[{"name": "setup", "error": "No test file found"}]
            )
        
        # Run pytest with JSON output
        try:
            cmd = [
                sys.executable, "-m", "pytest",
                str(test_file),
                "-v",
                "--tb=short",
                "-q"
            ]
            # Add timeout only if pytest-timeout is available
            try:
                import pytest_timeout
                cmd.append(f"--timeout={timeout}")
            except ImportError:
                pass  # pytest-timeout not installed, skip timeout flag
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 10,
                cwd=str(self.base_dir)
            )
            
            output = result.stdout + result.stderr
            
            # Parse results from output
            passed, failed, errors = self._parse_pytest_output(output)
            
            # Extract failed test details
            failed_tests = self._extract_failed_tests(output)
            
            return TestResult(
                problem=problem_path,
                passed=passed,
                failed=failed,
                errors=errors,
                total=passed + failed + errors,
                duration=0.0,  # Could parse from pytest output
                output=output,
                failed_tests=failed_tests
            )
            
        except subprocess.TimeoutExpired:
            return TestResult(
                problem=problem_path,
                passed=0, failed=0, errors=1, total=1,
                duration=timeout,
                output=f"Tests timed out after {timeout} seconds",
                failed_tests=[{"name": "timeout", "error": "Execution timeout"}]
            )
        except Exception as e:
            return TestResult(
                problem=problem_path,
                passed=0, failed=0, errors=1, total=1,
                duration=0.0,
                output=str(e),
                failed_tests=[{"name": "error", "error": str(e)}]
            )
    
    def _parse_pytest_output(self, output: str) -> Tuple[int, int, int]:
        """Parse pytest output for pass/fail/error counts."""
        import re
        
        # Look for summary line like "5 passed, 2 failed, 1 error"
        passed = failed = errors = 0
        
        # Match "X passed"
        match = re.search(r'(\d+) passed', output)
        if match:
            passed = int(match.group(1))
        
        # Match "X failed"
        match = re.search(r'(\d+) failed', output)
        if match:
            failed = int(match.group(1))
        
        # Match "X error"
        match = re.search(r'(\d+) error', output)
        if match:
            errors = int(match.group(1))
        
        return passed, failed, errors
    
    def _extract_failed_tests(self, output: str) -> List[Dict]:
        """Extract details of failed tests."""
        failed_tests = []
        
        # Simple extraction: look for FAILED lines
        import re
        for match in re.finditer(r'FAILED\s+(\S+)', output):
            test_name = match.group(1)
            failed_tests.append({
                "name": test_name,
                "error": "See output for details"
            })
        
        return failed_tests
    
    def display_result(self, result: TestResult):
        """Display test results."""
        if self.console and RICH_AVAILABLE:
            self._display_rich(result)
        else:
            self._display_simple(result)
    
    def _display_rich(self, result: TestResult):
        """Display results with rich formatting."""
        # Status color
        if result.failed == 0 and result.errors == 0 and result.passed > 0:
            status_style = "green"
            status_text = "✅ ALL TESTS PASSED"
        elif result.errors > 0:
            status_style = "red"
            status_text = "❌ ERRORS"
        else:
            status_style = "yellow"
            status_text = "⚠️ SOME TESTS FAILED"
        
        # Summary table
        table = Table(show_header=False, box=None)
        table.add_column(justify="right", style="dim")
        table.add_column(justify="left")
        
        table.add_row("Problem:", f"[bold]{result.problem}[/]")
        table.add_row("Passed:", f"[green]{result.passed}[/]")
        table.add_row("Failed:", f"[red]{result.failed}[/]")
        table.add_row("Errors:", f"[red]{result.errors}[/]")
        table.add_row("Total:", f"{result.total}")
        
        self.console.print(Panel(
            table,
            title=f"[{status_style}]{status_text}[/]",
            border_style=status_style
        ))
        
        # Show failed tests
        if result.failed_tests:
            self.console.print("\n[bold red]Failed Tests:[/]")
            for test in result.failed_tests:
                self.console.print(f"  • {test['name']}")
        
        # Show output if there are failures
        if result.failed > 0 or result.errors > 0:
            self.console.print("\n[dim]Test Output:[/]")
            self.console.print(Panel(result.output[-2000:], border_style="dim"))
    
    def _display_simple(self, result: TestResult):
        """Display results with simple formatting."""
        print(f"\n{'='*50}")
        print(f"TEST RESULTS: {result.problem}")
        print(f"{'='*50}")
        print(f"Passed: {result.passed}")
        print(f"Failed: {result.failed}")
        print(f"Errors: {result.errors}")
        print(f"Total:  {result.total}")
        
        if result.failed == 0 and result.errors == 0 and result.passed > 0:
            print("\n✅ ALL TESTS PASSED")
        else:
            print("\n❌ SOME TESTS FAILED")
            print("\nFailed Tests:")
            for test in result.failed_tests:
                print(f"  - {test['name']}")
            print("\nOutput:")
            print(result.output[-1000:])
        
        print(f"{'='*50}\n")


def run_problem_tests(problem_path: str) -> TestResult:
    """Convenience function to run tests for a problem."""
    runner = TestRunner()
    result = runner.run_tests(problem_path)
    runner.display_result(result)
    return result


# =============================================================================
# CLI
# =============================================================================

import click


@click.command()
@click.argument("problem", required=False)
@click.option("--all", "-a", "run_all", is_flag=True, help="Run all tests")
@click.option("--quiet", "-q", is_flag=True, help="Only show summary")
def main(problem: Optional[str], run_all: bool, quiet: bool):
    """
    Run tests for a problem.
    
    Examples:
        python -m cli.testing hashmap/problem_01_group_anagrams
        python -m cli.testing --all
    """
    runner = TestRunner()
    
    if run_all:
        # Find all problems and run tests
        all_results = []
        for pattern_dir in runner.problems_dir.iterdir():
            if pattern_dir.is_dir() and not pattern_dir.name.startswith('.'):
                for problem_dir in pattern_dir.iterdir():
                    if problem_dir.is_dir():
                        problem_path = f"{pattern_dir.name}/{problem_dir.name}"
                        result = runner.run_tests(problem_path)
                        all_results.append(result)
                        if not quiet:
                            runner.display_result(result)
        
        # Summary
        total_passed = sum(r.passed for r in all_results)
        total_failed = sum(r.failed for r in all_results)
        total_errors = sum(r.errors for r in all_results)
        
        print(f"\n{'='*50}")
        print(f"OVERALL: {total_passed} passed, {total_failed} failed, {total_errors} errors")
        print(f"{'='*50}\n")
        
    elif problem:
        result = runner.run_tests(problem)
        runner.display_result(result)
    else:
        print("Usage: python -m cli.testing <problem_path>")
        print("       python -m cli.testing --all")


if __name__ == "__main__":
    main()

