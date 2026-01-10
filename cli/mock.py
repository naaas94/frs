"""
Full Mock Interview Simulator

Runs a complete mock interview with random problem selection.

Usage:
    python -m cli.mock
    python -m cli.mock --duration 45
    python -m cli.mock --pattern hashmap
"""

import random
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import yaml

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from cli.timer import InterviewTimer, load_config


class MockInterview:
    """Full mock interview simulator."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.base_dir = Path(__file__).parent.parent
        self.problems_dir = self.base_dir / "problems"
        self.config = load_config()
    
    def get_available_problems(self, pattern: Optional[str] = None) -> List[Dict]:
        """Get list of available problems."""
        problems = []
        
        if not self.problems_dir.exists():
            return problems
        
        for pattern_dir in self.problems_dir.iterdir():
            if not pattern_dir.is_dir() or pattern_dir.name.startswith('.'):
                continue
            
            if pattern and pattern_dir.name != pattern:
                continue
            
            for problem_dir in pattern_dir.iterdir():
                if problem_dir.is_dir():
                    problem_file = problem_dir / "problem.md"
                    if problem_file.exists():
                        with open(problem_file) as f:
                            content = f.read()
                        lines = content.strip().split("\n")
                        title = lines[0].lstrip("#").strip() if lines else problem_dir.name
                        
                        problems.append({
                            "pattern": pattern_dir.name,
                            "name": title,
                            "path": f"{pattern_dir.name}/{problem_dir.name}",
                            "dir": problem_dir
                        })
        
        return problems
    
    def select_problem(self, pattern: Optional[str] = None) -> Optional[Dict]:
        """Select a random problem for the mock."""
        problems = self.get_available_problems(pattern)
        
        if not problems:
            return None
        
        # Weight towards mixed patterns for realistic mock
        if not pattern:
            # Prefer problems from different patterns
            patterns = list(set(p["pattern"] for p in problems))
            selected_pattern = random.choice(patterns)
            problems = [p for p in problems if p["pattern"] == selected_pattern]
        
        return random.choice(problems)
    
    def display_problem(self, problem: Dict):
        """Display the problem statement."""
        problem_file = problem["dir"] / "problem.md"
        
        if problem_file.exists():
            with open(problem_file) as f:
                content = f.read()
            
            if self.console and RICH_AVAILABLE:
                from rich.markdown import Markdown
                self.console.print(Panel(
                    Markdown(content),
                    title=f"📋 {problem['name']}",
                    border_style="cyan",
                    padding=(1, 2)
                ))
            else:
                print(f"\n{'='*60}")
                print(f"PROBLEM: {problem['name']}")
                print(f"{'='*60}")
                print(content)
                print(f"{'='*60}\n")
    
    def run_mock(self, duration: int = 35, pattern: Optional[str] = None) -> Dict:
        """Run a full mock interview."""
        # Select problem
        problem = self.select_problem(pattern)
        
        if not problem:
            if self.console:
                self.console.print("[red]No problems found in problem bank.[/]")
                self.console.print("[dim]Run: Create problems in problems/ directory[/]")
            else:
                print("No problems found. Create problems in problems/ directory.")
            return {"status": "no_problems"}
        
        # Introduction
        if self.console and RICH_AVAILABLE:
            self.console.print(Panel(
                "[bold]MOCK INTERVIEW[/]\n\n"
                f"Duration: [cyan]{duration} minutes[/]\n"
                f"Pattern: [yellow]{problem['pattern']}[/]\n\n"
                "[dim]This simulates a real interview environment.[/]\n"
                "[dim]No notes, talk aloud, write tests first.[/]\n\n"
                "[bold green]Press Enter when ready to see the problem...[/]",
                title="🎯 FRS Mock Interview",
                border_style="green"
            ))
        else:
            print(f"\n{'='*60}")
            print("MOCK INTERVIEW")
            print(f"Duration: {duration} minutes")
            print(f"Pattern: {problem['pattern']}")
            print(f"{'='*60}")
            print("\nPress Enter when ready to see the problem...")
        
        try:
            input()
        except KeyboardInterrupt:
            print("\nMock cancelled.")
            return {"status": "cancelled"}
        
        # Show problem
        self.display_problem(problem)
        
        # Give time to read
        if self.console:
            self.console.print("\n[dim]Take a moment to read the problem.[/]")
            self.console.print("[bold green]Press Enter to start the timer...[/]")
        else:
            print("\nTake a moment to read the problem.")
            print("Press Enter to start the timer...")
        
        try:
            input()
        except KeyboardInterrupt:
            print("\nMock cancelled.")
            return {"status": "cancelled"}
        
        # Run timer
        timer = InterviewTimer(self.config, problem["name"])
        session = timer.run()
        
        # Mock complete
        if self.console and RICH_AVAILABLE:
            self.console.print(Panel(
                "[bold]Mock Interview Complete![/]\n\n"
                f"Problem: [cyan]{problem['name']}[/]\n"
                f"Pattern: [yellow]{problem['pattern']}[/]\n\n"
                "[bold yellow]Next steps:[/]\n"
                "1. Run your tests: [dim]python -m cli.testing " + problem['path'] + "[/]\n"
                "2. Record postmortem: [dim]python -m cli.postmortem[/]\n"
                "3. Review your solution",
                title="✅ Mock Complete",
                border_style="green"
            ))
        else:
            print(f"\n{'='*60}")
            print("MOCK COMPLETE")
            print(f"Problem: {problem['name']}")
            print(f"Pattern: {problem['pattern']}")
            print(f"{'='*60}")
            print("\nNext steps:")
            print(f"1. Run tests: python -m cli.testing {problem['path']}")
            print("2. Record postmortem: python -m cli.postmortem")
            print("3. Review your solution")
        
        return {
            "status": "completed",
            "problem": problem,
            "session": session
        }


# =============================================================================
# CLI
# =============================================================================

import click


@click.command()
@click.option("--duration", "-t", type=int, default=35, help="Duration in minutes")
@click.option("--pattern", "-p", type=str, help="Specific pattern to practice")
@click.option("--list-problems", "-l", is_flag=True, help="List available problems")
def main(duration: int, pattern: Optional[str], list_problems: bool):
    """
    Run a full mock interview.
    
    Simulates a real interview environment with:
    - Random problem selection
    - Timed session with stage prompts
    - No notes, talk aloud, tests first
    
    Examples:
        python -m cli.mock
        python -m cli.mock --duration 45
        python -m cli.mock --pattern hashmap
    """
    mock = MockInterview()
    
    if list_problems:
        problems = mock.get_available_problems(pattern)
        if mock.console and RICH_AVAILABLE:
            table = Table(title="Available Problems")
            table.add_column("Pattern", style="cyan")
            table.add_column("Problem", style="white")
            table.add_column("Path", style="dim")
            
            for p in problems:
                table.add_row(p["pattern"], p["name"], p["path"])
            
            mock.console.print(table)
        else:
            print("\nAvailable Problems:")
            for p in problems:
                print(f"  [{p['pattern']}] {p['name']}")
        return
    
    result = mock.run_mock(duration=duration, pattern=pattern)
    
    if result.get("status") == "completed":
        # Prompt for postmortem
        if mock.console:
            if Confirm.ask("\n[yellow]Record postmortem now?[/]", default=True):
                from cli.postmortem import PostmortemCapture
                capture = PostmortemCapture()
                pm = capture.capture(result["problem"]["name"])
                filepath = capture.save(pm)
                capture.display_summary(pm, filepath)


if __name__ == "__main__":
    main()

