"""
Full Mock Interview Simulator

Runs a complete mock interview with random problem selection.

Usage:
    python -m cli.mock
    python -m cli.mock --duration 45
    python -m cli.mock --pattern hashmap
    python -m cli.mock --mode aie --pattern fastapi
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
        self.aie_prompts_dir = self.base_dir / "aie" / "00_sprint_hub" / "mock_prompts"
        self.config = load_config()
    
    def _parse_aie_prompt(self, prompt_file: Path) -> Optional[Dict]:
        """Parse a markdown prompt file into a mock problem dict."""
        if not prompt_file.exists():
            return None

        with open(prompt_file) as f:
            content = f.read()

        lines = [line.strip() for line in content.splitlines() if line.strip()]
        title = prompt_file.stem.replace("_", " ").title()
        pattern = "aie_general"

        for line in lines:
            if line.startswith("# ") and title == prompt_file.stem.replace("_", " ").title():
                title = line.lstrip("#").strip()
                continue
            lower = line.lower()
            if lower.startswith("pattern:") or lower.startswith("- pattern:"):
                pattern = line.split(":", 1)[1].strip().lower().replace(" ", "_")
                break

        return {
            "pattern": pattern,
            "name": title,
            "path": f"aie/00_sprint_hub/mock_prompts/{prompt_file.name}",
            "dir": prompt_file.parent,
            "file": prompt_file,
            "content": content,
            "mode": "aie",
        }

    def get_available_aie_prompts(self, pattern: Optional[str] = None) -> List[Dict]:
        """Get list of available AIE mock prompts."""
        prompts: List[Dict] = []
        if not self.aie_prompts_dir.exists():
            return prompts

        for prompt_file in sorted(self.aie_prompts_dir.glob("*.md")):
            parsed = self._parse_aie_prompt(prompt_file)
            if not parsed:
                continue
            if pattern and parsed["pattern"] != pattern:
                continue
            prompts.append(parsed)

        return prompts

    def get_available_problems(self, pattern: Optional[str] = None, mode: str = "core") -> List[Dict]:
        """Get list of available problems for a track."""
        if mode == "aie":
            return self.get_available_aie_prompts(pattern)

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
                            "dir": problem_dir,
                            "mode": "core",
                        })
        
        return problems
    
    def select_problem(self, pattern: Optional[str] = None, mode: str = "core") -> Optional[Dict]:
        """Select a random problem for the mock."""
        problems = self.get_available_problems(pattern, mode=mode)
        
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
        if problem.get("mode") == "aie":
            content = problem.get("content", "")
        else:
            problem_file = problem["dir"] / "problem.md"
            content = ""
            if problem_file.exists():
                with open(problem_file) as f:
                    content = f.read()
        
        if content:
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

    def _save_session_metadata(self, session: Dict):
        """Persist custom mock metadata into the latest session log."""
        sessions_dir = self.base_dir / "logs" / "sessions"
        if not sessions_dir.exists():
            return

        session_files = sorted(sessions_dir.glob("*.json"), reverse=True)
        if not session_files:
            return

        for file_path in session_files[:5]:
            try:
                with open(file_path) as f:
                    data = json.load(f)
                if data.get("start_time") == session.get("start_time"):
                    data.update(
                        {
                            "track_mode": session.get("track_mode"),
                            "pattern": session.get("pattern"),
                            "problem_path": session.get("problem_path"),
                        }
                    )
                    with open(file_path, "w") as f:
                        json.dump(data, f, indent=2)
                    return
            except Exception:
                continue
    
    def run_mock(self, duration: int = 35, pattern: Optional[str] = None, mode: str = "core") -> Dict:
        """Run a full mock interview."""
        # Select problem
        problem = self.select_problem(pattern, mode=mode)
        
        if not problem:
            if self.console:
                source_path = "problems/" if mode == "core" else "aie/00_sprint_hub/mock_prompts/"
                self.console.print("[red]No mock prompts found.[/]")
                self.console.print(f"[dim]Add prompts under: {source_path}[/]")
            else:
                source_path = "problems/" if mode == "core" else "aie/00_sprint_hub/mock_prompts/"
                print(f"No prompts found. Add prompt files under {source_path}.")
            return {"status": "no_problems"}
        
        # Introduction
        mock_title = "AIE MOCK INTERVIEW" if mode == "aie" else "MOCK INTERVIEW"
        if self.console and RICH_AVAILABLE:
            self.console.print(Panel(
                f"[bold]{mock_title}[/]\n\n"
                f"Duration: [cyan]{duration} minutes[/]\n"
                f"Pattern: [yellow]{problem['pattern']}[/]\n\n"
                "[dim]This simulates a real interview environment.[/]\n"
                "[dim]No notes, talk aloud, write tests first.[/]\n\n"
                "[bold green]Press Enter when ready to see the problem...[/]",
                title="🎯 FRS Mock",
                border_style="green"
            ))
        else:
            print(f"\n{'='*60}")
            print(mock_title)
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
        session["track_mode"] = mode
        session["pattern"] = problem["pattern"]
        session["problem_path"] = problem["path"]
        self._save_session_metadata(session)
        
        # Mock complete
        if self.console and RICH_AVAILABLE:
            if mode == "core":
                next_step_tests = "1. Run your tests: [dim]python -m cli.testing " + problem['path'] + "[/]\n"
            else:
                next_step_tests = "1. Implement in a scratch file and run your checks\n"
            self.console.print(Panel(
                (
                    "[bold]Mock Interview Complete![/]\n\n"
                    f"Problem: [cyan]{problem['name']}[/]\n"
                    f"Pattern: [yellow]{problem['pattern']}[/]\n\n"
                    "[bold yellow]Next steps:[/]\n"
                    + next_step_tests
                    + "2. Record postmortem: [dim]python -m cli.postmortem[/]\n"
                    + "3. Review your solution"
                ),
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
            if mode == "core":
                print(f"1. Run tests: python -m cli.testing {problem['path']}")
            else:
                print("1. Implement in a scratch file and run your checks")
            print("2. Record postmortem: python -m cli.postmortem")
            print("3. Review your solution")
        
        return {
            "status": "completed",
            "problem": problem,
            "session": session,
            "mode": mode,
        }


# =============================================================================
# CLI
# =============================================================================

import click


@click.command()
@click.option("--duration", "-t", type=int, default=35, help="Duration in minutes")
@click.option("--pattern", "-p", type=str, help="Specific pattern to practice")
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["core", "aie"]),
    default="core",
    show_default=True,
    help="Mock track: core problems or AIE prompts",
)
@click.option("--list-problems", "-l", is_flag=True, help="List available problems")
def main(duration: int, pattern: Optional[str], mode: str, list_problems: bool):
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
        python -m cli.mock --mode aie --pattern fastapi
    """
    mock = MockInterview()
    
    if list_problems:
        problems = mock.get_available_problems(pattern, mode=mode)
        if mock.console and RICH_AVAILABLE:
            table_title = "Available AIE Prompts" if mode == "aie" else "Available Problems"
            table = Table(title=table_title)
            table.add_column("Pattern", style="cyan")
            table.add_column("Problem", style="white")
            table.add_column("Path", style="dim")
            
            for p in problems:
                table.add_row(p["pattern"], p["name"], p["path"])
            
            mock.console.print(table)
        else:
            header = "\nAvailable AIE Prompts:" if mode == "aie" else "\nAvailable Problems:"
            print(header)
            for p in problems:
                print(f"  [{p['pattern']}] {p['name']}")
        return
    
    result = mock.run_mock(duration=duration, pattern=pattern, mode=mode)
    
    if result.get("status") == "completed":
        # Prompt for postmortem
        if mock.console:
            if Confirm.ask("\n[yellow]Record postmortem now?[/]", default=True):
                from cli.postmortem import PostmortemCapture
                capture = PostmortemCapture()
                pm = capture.capture(
                    result["problem"]["name"],
                    track_mode=result.get("mode"),
                    aie_pattern_hint=result["problem"].get("pattern"),
                )
                filepath = capture.save(pm)
                capture.display_summary(pm, filepath)


if __name__ == "__main__":
    main()

