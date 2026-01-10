"""
Postmortem Capture CLI

Interactive 5-line postmortem after each coding session.

Usage:
    python -m cli.postmortem
    python -m cli.postmortem --problem "group anagrams"
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import yaml

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# =============================================================================
# CONFIGURATION
# =============================================================================

def load_config() -> Dict:
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


PATTERNS = [
    "hashmap",
    "two_pointers",
    "sorting",
    "heap",
    "binary_search",
    "graph",
    "plumbing",
    "mixed",
    "other"
]

BUG_CLASSES = [
    "off-by-one",
    "missing edge case",
    "wrong invariant",
    "Python API slip",
    "logic error",
    "time complexity",
    "space complexity",
    "no bugs"
]


# =============================================================================
# POSTMORTEM CLASS
# =============================================================================

class PostmortemCapture:
    """Interactive postmortem capture."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.base_dir = Path(__file__).parent.parent
        self.logs_dir = self.base_dir / "logs" / "postmortems"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Load last session
        self.last_session = self._load_last_session()
    
    def _load_last_session(self) -> Optional[Dict]:
        """Load the most recent session log."""
        sessions_dir = self.base_dir / "logs" / "sessions"
        if not sessions_dir.exists():
            return None
        
        session_files = sorted(sessions_dir.glob("*.json"), reverse=True)
        if session_files:
            with open(session_files[0]) as f:
                return json.load(f)
        return None
    
    def capture_rich(self, problem_override: Optional[str] = None) -> Dict:
        """Capture postmortem with rich prompts."""
        self.console.print(Panel(
            "[bold cyan]POST-MORTEM CAPTURE[/]\n\n"
            "Answer 5 questions to convert this session into learning.\n"
            "This takes 2-3 minutes and prevents repeating mistakes.",
            title="📝 Postmortem",
            border_style="cyan"
        ))
        
        # Get problem name
        default_problem = "Unknown Problem"
        if self.last_session:
            default_problem = self.last_session.get("problem", default_problem)
        if problem_override:
            default_problem = problem_override
        
        problem = Prompt.ask(
            "\n[bold]1. Problem name[/]",
            default=default_problem
        )
        
        # Pattern used
        self.console.print("\n[bold]2. Pattern used[/]")
        for i, pattern in enumerate(PATTERNS, 1):
            self.console.print(f"   {i}. {pattern}")
        
        pattern_idx = Prompt.ask(
            "Select pattern (number)",
            choices=[str(i) for i in range(1, len(PATTERNS) + 1)],
            default="1"
        )
        pattern_used = PATTERNS[int(pattern_idx) - 1]
        
        # Bug class
        self.console.print("\n[bold]3. Primary bug class[/]")
        for i, bug in enumerate(BUG_CLASSES, 1):
            self.console.print(f"   {i}. {bug}")
        
        bug_idx = Prompt.ask(
            "Select bug class (number)",
            choices=[str(i) for i in range(1, len(BUG_CLASSES) + 1)],
            default="8"
        )
        bug_class = BUG_CLASSES[int(bug_idx) - 1]
        
        # Fix rule
        self.console.print()
        fix_rule = Prompt.ask(
            "[bold]4. Fix rule[/] (one sentence to prevent this bug)",
            default="N/A" if bug_class == "no bugs" else ""
        )
        
        # Micro-drill
        self.console.print()
        micro_drill = Prompt.ask(
            "[bold]5. Micro-drill[/] (5-min exercise to practice tomorrow)",
            default="Review pattern template"
        )
        
        # Bonus: new test case
        self.console.print()
        new_test = Prompt.ask(
            "[dim]Bonus: New test case that would have caught the bug[/]",
            default=""
        )
        
        # Additional notes
        self.console.print()
        notes = Prompt.ask(
            "[dim]Any additional notes?[/]",
            default=""
        )
        
        # Confidence rating
        confidence = Prompt.ask(
            "\n[bold]Confidence with this pattern (1-5)[/]",
            choices=["1", "2", "3", "4", "5"],
            default="3"
        )
        
        postmortem = {
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "pattern_used": pattern_used,
            "bug_class": bug_class,
            "fix_rule": fix_rule,
            "micro_drill": micro_drill,
            "new_test_case": new_test,
            "notes": notes,
            "confidence": int(confidence),
            "session": self.last_session.get("start_time") if self.last_session else None
        }
        
        return postmortem
    
    def capture_simple(self, problem_override: Optional[str] = None) -> Dict:
        """Capture postmortem with simple prompts."""
        print("\n" + "="*50)
        print("POST-MORTEM CAPTURE")
        print("="*50)
        
        # Get problem name
        default_problem = "Unknown Problem"
        if self.last_session:
            default_problem = self.last_session.get("problem", default_problem)
        if problem_override:
            default_problem = problem_override
        
        problem = input(f"\n1. Problem name [{default_problem}]: ").strip() or default_problem
        
        # Pattern used
        print("\n2. Pattern used:")
        for i, pattern in enumerate(PATTERNS, 1):
            print(f"   {i}. {pattern}")
        pattern_idx = input("Select pattern (number) [1]: ").strip() or "1"
        pattern_used = PATTERNS[int(pattern_idx) - 1]
        
        # Bug class
        print("\n3. Primary bug class:")
        for i, bug in enumerate(BUG_CLASSES, 1):
            print(f"   {i}. {bug}")
        bug_idx = input("Select bug class (number) [8]: ").strip() or "8"
        bug_class = BUG_CLASSES[int(bug_idx) - 1]
        
        # Fix rule
        default_fix = "N/A" if bug_class == "no bugs" else ""
        fix_rule = input(f"\n4. Fix rule (one sentence) [{default_fix}]: ").strip() or default_fix
        
        # Micro-drill
        micro_drill = input("\n5. Micro-drill (5-min exercise for tomorrow): ").strip() or "Review pattern template"
        
        # Bonus
        new_test = input("\nBonus - New test case that would have caught it: ").strip()
        notes = input("Any additional notes: ").strip()
        confidence = input("Confidence with this pattern (1-5) [3]: ").strip() or "3"
        
        postmortem = {
            "timestamp": datetime.now().isoformat(),
            "problem": problem,
            "pattern_used": pattern_used,
            "bug_class": bug_class,
            "fix_rule": fix_rule,
            "micro_drill": micro_drill,
            "new_test_case": new_test,
            "notes": notes,
            "confidence": int(confidence),
            "session": self.last_session.get("start_time") if self.last_session else None
        }
        
        return postmortem
    
    def capture(self, problem_override: Optional[str] = None) -> Dict:
        """Capture postmortem using best available UI."""
        if RICH_AVAILABLE and self.console:
            return self.capture_rich(problem_override)
        else:
            return self.capture_simple(problem_override)
    
    def save(self, postmortem: Dict) -> Path:
        """Save postmortem to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_problem = postmortem["problem"].replace("/", "_").replace(" ", "_")[:30]
        filename = f"{timestamp}_{safe_problem}.json"
        
        filepath = self.logs_dir / filename
        with open(filepath, "w") as f:
            json.dump(postmortem, f, indent=2)
        
        # Also save as markdown for easy reading
        md_filepath = filepath.with_suffix(".md")
        self._save_markdown(postmortem, md_filepath)
        
        # Update metrics
        self._update_metrics(postmortem)
        
        return filepath
    
    def _save_markdown(self, postmortem: Dict, filepath: Path):
        """Save postmortem as readable markdown."""
        md_content = f"""# Post-Mortem: {postmortem['problem']}

**Date:** {postmortem['timestamp'][:10]}

## Summary

| Field | Value |
|-------|-------|
| Pattern | {postmortem['pattern_used']} |
| Bug Class | {postmortem['bug_class']} |
| Confidence | {postmortem['confidence']}/5 |

## Fix Rule

{postmortem['fix_rule']}

## Micro-Drill (Tomorrow)

{postmortem['micro_drill']}

## New Test Case

{postmortem['new_test_case'] or 'N/A'}

## Notes

{postmortem['notes'] or 'N/A'}
"""
        with open(filepath, "w") as f:
            f.write(md_content)
    
    def _update_metrics(self, postmortem: Dict):
        """Update aggregate metrics."""
        metrics_file = self.base_dir / "logs" / "metrics.json"
        
        if metrics_file.exists():
            with open(metrics_file) as f:
                metrics = json.load(f)
        else:
            metrics = {
                "total_sessions": 0,
                "patterns": {},
                "bug_classes": {},
                "confidence_by_pattern": {},
                "daily_sessions": {},
                "micro_drills_pending": []
            }
        
        # Update counts
        metrics["total_sessions"] += 1
        
        pattern = postmortem["pattern_used"]
        metrics["patterns"][pattern] = metrics["patterns"].get(pattern, 0) + 1
        
        bug = postmortem["bug_class"]
        metrics["bug_classes"][bug] = metrics["bug_classes"].get(bug, 0) + 1
        
        # Update confidence (running average)
        if pattern not in metrics["confidence_by_pattern"]:
            metrics["confidence_by_pattern"][pattern] = {
                "total": 0,
                "count": 0,
                "average": 0
            }
        conf = metrics["confidence_by_pattern"][pattern]
        conf["total"] += postmortem["confidence"]
        conf["count"] += 1
        conf["average"] = conf["total"] / conf["count"]
        
        # Track daily sessions
        date = postmortem["timestamp"][:10]
        metrics["daily_sessions"][date] = metrics["daily_sessions"].get(date, 0) + 1
        
        # Add micro-drill to pending
        if postmortem["micro_drill"] and postmortem["micro_drill"] != "N/A":
            metrics["micro_drills_pending"].append({
                "drill": postmortem["micro_drill"],
                "pattern": pattern,
                "date": date
            })
            # Keep only last 10
            metrics["micro_drills_pending"] = metrics["micro_drills_pending"][-10:]
        
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)
    
    def display_summary(self, postmortem: Dict, filepath: Path):
        """Display saved postmortem summary."""
        if self.console and RICH_AVAILABLE:
            table = Table(show_header=False, box=None)
            table.add_column(justify="right", style="dim")
            table.add_column(justify="left")
            
            table.add_row("Problem:", f"[bold]{postmortem['problem']}[/]")
            table.add_row("Pattern:", f"[cyan]{postmortem['pattern_used']}[/]")
            table.add_row("Bug Class:", f"[yellow]{postmortem['bug_class']}[/]")
            table.add_row("Fix Rule:", postmortem['fix_rule'])
            table.add_row("Micro-Drill:", f"[green]{postmortem['micro_drill']}[/]")
            table.add_row("Confidence:", f"{postmortem['confidence']}/5")
            
            self.console.print(Panel(
                table,
                title="✅ Postmortem Saved",
                border_style="green"
            ))
            
            self.console.print(f"\n[dim]Saved to: {filepath}[/]")
            self.console.print("\n[bold yellow]Tomorrow's micro-drill:[/]")
            self.console.print(f"  → {postmortem['micro_drill']}\n")
        else:
            print("\n" + "="*50)
            print("✅ POSTMORTEM SAVED")
            print("="*50)
            print(f"Problem: {postmortem['problem']}")
            print(f"Pattern: {postmortem['pattern_used']}")
            print(f"Bug Class: {postmortem['bug_class']}")
            print(f"Fix Rule: {postmortem['fix_rule']}")
            print(f"Micro-Drill: {postmortem['micro_drill']}")
            print(f"\nSaved to: {filepath}")
            print(f"\nTomorrow's micro-drill: {postmortem['micro_drill']}\n")


# =============================================================================
# CLI
# =============================================================================

import click


@click.command()
@click.option("--problem", "-p", type=str, help="Problem name (override auto-detect)")
@click.option("--view-last", "-v", is_flag=True, help="View last postmortem")
def main(problem: Optional[str], view_last: bool):
    """
    Record a postmortem for your coding session.
    
    The 5-line postmortem:
    1. Pattern used
    2. Bug class (off-by-one, edge case, etc.)
    3. Fix rule (one sentence to prevent this bug)
    4. Micro-drill (5-min exercise for tomorrow)
    5. New test case that would have caught it
    
    Examples:
        python -m cli.postmortem
        python -m cli.postmortem --problem "Group Anagrams"
    """
    capture = PostmortemCapture()
    
    if view_last:
        # View last postmortem
        postmortems = sorted(capture.logs_dir.glob("*.json"), reverse=True)
        if postmortems:
            with open(postmortems[0]) as f:
                last = json.load(f)
            capture.display_summary(last, postmortems[0])
        else:
            print("No postmortems found.")
        return
    
    try:
        postmortem = capture.capture(problem)
        filepath = capture.save(postmortem)
        capture.display_summary(postmortem, filepath)
    except KeyboardInterrupt:
        print("\n\nPostmortem cancelled.")


if __name__ == "__main__":
    main()

