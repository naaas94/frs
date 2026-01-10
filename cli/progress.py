"""
Progress Dashboard

Visual dashboard showing sprint progress and metrics.

Usage:
    python -m cli.progress
    python -m cli.progress --detailed
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import Counter

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ProgressDashboard:
    """Progress tracking dashboard."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.base_dir = Path(__file__).parent.parent
        self.logs_dir = self.base_dir / "logs"
    
    def load_metrics(self) -> Dict:
        """Load aggregate metrics."""
        metrics_file = self.logs_dir / "metrics.json"
        
        if metrics_file.exists():
            with open(metrics_file) as f:
                return json.load(f)
        
        return {
            "total_sessions": 0,
            "patterns": {},
            "bug_classes": {},
            "confidence_by_pattern": {},
            "daily_sessions": {},
            "micro_drills_pending": []
        }
    
    def load_postmortems(self) -> List[Dict]:
        """Load all postmortems."""
        pm_dir = self.logs_dir / "postmortems"
        postmortems = []
        
        if pm_dir.exists():
            for f in pm_dir.glob("*.json"):
                with open(f) as fp:
                    postmortems.append(json.load(fp))
        
        return sorted(postmortems, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    def load_sessions(self) -> List[Dict]:
        """Load all session logs."""
        sessions_dir = self.logs_dir / "sessions"
        sessions = []
        
        if sessions_dir.exists():
            for f in sessions_dir.glob("*.json"):
                with open(f) as fp:
                    sessions.append(json.load(fp))
        
        return sorted(sessions, key=lambda x: x.get("start_time", ""), reverse=True)
    
    def calculate_streak(self) -> int:
        """Calculate current practice streak in days."""
        metrics = self.load_metrics()
        daily = metrics.get("daily_sessions", {})
        
        if not daily:
            return 0
        
        streak = 0
        today = datetime.now().date()
        
        # Check each day going backwards
        for i in range(365):  # Max 1 year
            date = (today - timedelta(days=i)).isoformat()
            if date in daily:
                streak += 1
            elif i > 0:  # Allow today to be missing
                break
        
        return streak
    
    def get_pattern_progress(self) -> Dict[str, Dict]:
        """Get progress for each pattern."""
        metrics = self.load_metrics()
        postmortems = self.load_postmortems()
        
        patterns = [
            "hashmap", "two_pointers", "sorting", "heap",
            "binary_search", "graph", "plumbing"
        ]
        
        progress = {}
        for pattern in patterns:
            count = metrics.get("patterns", {}).get(pattern, 0)
            conf = metrics.get("confidence_by_pattern", {}).get(pattern, {})
            avg_confidence = conf.get("average", 0)
            
            # Get recent bugs for this pattern
            pattern_pms = [pm for pm in postmortems if pm.get("pattern_used") == pattern]
            recent_bugs = [pm.get("bug_class") for pm in pattern_pms[:5]]
            
            progress[pattern] = {
                "sessions": count,
                "avg_confidence": round(avg_confidence, 1),
                "recent_bugs": recent_bugs,
                "status": self._get_pattern_status(count, avg_confidence)
            }
        
        return progress
    
    def _get_pattern_status(self, sessions: int, confidence: float) -> str:
        """Determine pattern status."""
        if sessions == 0:
            return "not_started"
        elif confidence >= 4.0 and sessions >= 3:
            return "mastered"
        elif confidence >= 3.0 or sessions >= 2:
            return "practicing"
        else:
            return "needs_work"
    
    def display_rich(self, detailed: bool = False):
        """Display dashboard with rich formatting."""
        metrics = self.load_metrics()
        streak = self.calculate_streak()
        pattern_progress = self.get_pattern_progress()
        
        # Header
        self.console.print(Panel(
            f"[bold cyan]INTERVIEW SPRINT DASHBOARD[/]\n\n"
            f"Total Sessions: [bold]{metrics.get('total_sessions', 0)}[/]  |  "
            f"Streak: [bold green]{streak} days[/]",
            title="📊 Progress",
            border_style="cyan"
        ))
        
        # Pattern Progress Table
        table = Table(title="Pattern Progress", box=box.ROUNDED)
        table.add_column("Pattern", style="cyan")
        table.add_column("Sessions", justify="center")
        table.add_column("Confidence", justify="center")
        table.add_column("Status", justify="center")
        
        status_styles = {
            "not_started": "[dim]Not Started[/]",
            "needs_work": "[red]Needs Work[/]",
            "practicing": "[yellow]Practicing[/]",
            "mastered": "[green]✓ Mastered[/]"
        }
        
        for pattern, data in pattern_progress.items():
            conf_display = f"{data['avg_confidence']}/5" if data['sessions'] > 0 else "-"
            conf_color = "green" if data['avg_confidence'] >= 4 else "yellow" if data['avg_confidence'] >= 3 else "red"
            
            table.add_row(
                pattern.replace("_", " ").title(),
                str(data['sessions']),
                f"[{conf_color}]{conf_display}[/]",
                status_styles.get(data['status'], data['status'])
            )
        
        self.console.print(table)
        
        # Bug Class Distribution
        bug_classes = metrics.get("bug_classes", {})
        if bug_classes:
            self.console.print("\n[bold]Bug Class Distribution:[/]")
            total_bugs = sum(bug_classes.values())
            for bug, count in sorted(bug_classes.items(), key=lambda x: -x[1])[:5]:
                pct = count / total_bugs * 100
                bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                self.console.print(f"  {bug:20} [{bar}] {count} ({pct:.0f}%)")
        
        # Pending Micro-Drills
        drills = metrics.get("micro_drills_pending", [])
        if drills:
            self.console.print("\n[bold yellow]Pending Micro-Drills:[/]")
            for drill in drills[-3:]:
                self.console.print(f"  → {drill['drill']} [dim]({drill['pattern']})[/]")
        
        # Weekly Activity
        daily = metrics.get("daily_sessions", {})
        if daily:
            self.console.print("\n[bold]Last 7 Days:[/]")
            today = datetime.now().date()
            week_display = []
            for i in range(6, -1, -1):
                date = (today - timedelta(days=i)).isoformat()
                count = daily.get(date, 0)
                day_name = (today - timedelta(days=i)).strftime("%a")
                if count > 0:
                    week_display.append(f"[green]{day_name}:{count}[/]")
                else:
                    week_display.append(f"[dim]{day_name}:0[/]")
            self.console.print("  " + "  ".join(week_display))
        
        # Detailed view
        if detailed:
            postmortems = self.load_postmortems()
            if postmortems:
                self.console.print("\n[bold]Recent Postmortems:[/]")
                detail_table = Table(box=box.SIMPLE)
                detail_table.add_column("Date")
                detail_table.add_column("Problem")
                detail_table.add_column("Pattern")
                detail_table.add_column("Bug")
                detail_table.add_column("Conf")
                
                for pm in postmortems[:10]:
                    date = pm.get("timestamp", "")[:10]
                    detail_table.add_row(
                        date,
                        pm.get("problem", "")[:25],
                        pm.get("pattern_used", ""),
                        pm.get("bug_class", ""),
                        str(pm.get("confidence", ""))
                    )
                
                self.console.print(detail_table)
        
        # Sprint Status
        self.console.print()
        total_sessions = metrics.get("total_sessions", 0)
        if total_sessions >= 14:
            self.console.print(Panel(
                "[bold green]🎉 Sprint Complete![/]\n\n"
                "You've completed the 14-day sprint.\n"
                "Review your progress and continue practicing weak patterns.",
                border_style="green"
            ))
        else:
            days_remaining = 14 - min(total_sessions, 14)
            self.console.print(Panel(
                f"[bold]Sprint Progress: {total_sessions}/14 days[/]\n\n"
                f"[{'█' * total_sessions}{'░' * days_remaining}]\n\n"
                f"[dim]{days_remaining} sessions remaining[/]",
                border_style="yellow"
            ))
    
    def display_simple(self, detailed: bool = False):
        """Display dashboard with simple formatting."""
        metrics = self.load_metrics()
        streak = self.calculate_streak()
        pattern_progress = self.get_pattern_progress()
        
        print("\n" + "="*60)
        print("INTERVIEW SPRINT DASHBOARD")
        print("="*60)
        print(f"Total Sessions: {metrics.get('total_sessions', 0)}")
        print(f"Current Streak: {streak} days")
        
        print("\n--- Pattern Progress ---")
        for pattern, data in pattern_progress.items():
            status = "✓" if data['status'] == 'mastered' else " "
            print(f"  [{status}] {pattern:15} Sessions: {data['sessions']:2}  Confidence: {data['avg_confidence']}/5")
        
        bug_classes = metrics.get("bug_classes", {})
        if bug_classes:
            print("\n--- Top Bug Classes ---")
            for bug, count in sorted(bug_classes.items(), key=lambda x: -x[1])[:5]:
                print(f"  {bug}: {count}")
        
        drills = metrics.get("micro_drills_pending", [])
        if drills:
            print("\n--- Pending Micro-Drills ---")
            for drill in drills[-3:]:
                print(f"  → {drill['drill']}")
        
        print("\n" + "="*60 + "\n")
    
    def display(self, detailed: bool = False):
        """Display dashboard using best available UI."""
        if RICH_AVAILABLE and self.console:
            self.display_rich(detailed)
        else:
            self.display_simple(detailed)


# =============================================================================
# CLI
# =============================================================================

import click


@click.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed view")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def main(detailed: bool, as_json: bool):
    """
    View your sprint progress dashboard.
    
    Shows:
    - Pattern-by-pattern progress
    - Confidence levels
    - Bug class distribution
    - Practice streak
    - Pending micro-drills
    
    Examples:
        python -m cli.progress
        python -m cli.progress --detailed
    """
    dashboard = ProgressDashboard()
    
    if as_json:
        metrics = dashboard.load_metrics()
        metrics["streak"] = dashboard.calculate_streak()
        metrics["pattern_progress"] = dashboard.get_pattern_progress()
        print(json.dumps(metrics, indent=2))
    else:
        dashboard.display(detailed)


if __name__ == "__main__":
    main()

