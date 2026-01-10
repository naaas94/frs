"""
Interview Timer CLI

Timed coding sessions with stage prompts and stress management interrupts.

Usage:
    python -m cli.timer --day 1
    python -m cli.timer --problem hashmap/problem_01_group_anagrams
    python -m cli.timer --duration 30
"""

import time
import sys
import os
import json
import yaml
import click
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Warning: 'rich' not installed. Run: pip install rich")


# =============================================================================
# CONFIGURATION
# =============================================================================

def load_config() -> Dict:
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return get_default_config()


def get_default_config() -> Dict:
    """Default configuration if config.yaml not found."""
    return {
        "timer": {
            "default_duration_minutes": 35,
            "stages": [
                {"name": "RESTATE & PICK PATTERN", "duration_minutes": 2,
                 "prompt": "Restate the problem. What pattern fits?"},
                {"name": "WRITE TESTS FIRST", "duration_minutes": 2,
                 "prompt": "Write 2-3 test cases before implementation."},
                {"name": "BASELINE IMPLEMENTATION", "duration_minutes": 15,
                 "prompt": "Implement the simplest correct solution."},
                {"name": "EDGE CASES & CLEANUP", "duration_minutes": 5,
                 "prompt": "Handle edge cases. Clean up code."},
                {"name": "BUFFER", "duration_minutes": 11,
                 "prompt": "Optimize if time permits."},
            ],
            "interrupts": {
                "baseline_reminder": {
                    "at_minute": 4,
                    "message": "🧊 FREEZE → BASELINE: Implement the simplest correct solution first."
                },
                "invariant_anchor": {
                    "at_minute": 10,
                    "message": "🎯 RE-ANCHOR: What must be true after each step? State your invariant."
                }
            },
            "audio_enabled": True
        }
    }


# =============================================================================
# AUDIO ALERTS
# =============================================================================

def play_alert(alert_type: str = "stage"):
    """Play audio alert for stage transitions."""
    try:
        # Try system beep first (cross-platform)
        if sys.platform == "win32":
            import winsound
            if alert_type == "interrupt":
                winsound.Beep(800, 500)
                winsound.Beep(800, 500)
            else:
                winsound.Beep(1000, 200)
        else:
            # Unix-like systems
            print("\a", end="", flush=True)
    except Exception:
        pass  # Silent fail if audio not available


# =============================================================================
# TIMER DISPLAY
# =============================================================================

class InterviewTimer:
    """Main timer class with stage management."""
    
    def __init__(self, config: Dict, problem_name: str = "Practice Problem"):
        self.config = config["timer"]
        self.problem_name = problem_name
        self.stages = self.config["stages"]
        self.interrupts = self.config.get("interrupts", {})
        self.audio_enabled = self.config.get("audio_enabled", True)
        self.total_duration = sum(s["duration_minutes"] for s in self.stages) * 60
        
        self.console = Console() if RICH_AVAILABLE else None
        self.start_time = None
        self.current_stage_idx = 0
        self.triggered_interrupts = set()
        
        # Session log
        self.session_log = {
            "problem": problem_name,
            "start_time": None,
            "end_time": None,
            "stages": [],
            "interrupts_shown": []
        }
    
    def get_current_stage(self, elapsed_seconds: int) -> tuple:
        """Get current stage based on elapsed time."""
        cumulative = 0
        for idx, stage in enumerate(self.stages):
            stage_duration = stage["duration_minutes"] * 60
            if elapsed_seconds < cumulative + stage_duration:
                stage_elapsed = elapsed_seconds - cumulative
                stage_remaining = stage_duration - stage_elapsed
                return idx, stage, stage_elapsed, stage_remaining
            cumulative += stage_duration
        
        # Past all stages
        last_stage = self.stages[-1]
        return len(self.stages) - 1, last_stage, 0, 0
    
    def check_interrupts(self, elapsed_minutes: int) -> Optional[str]:
        """Check if any interrupt should fire."""
        for name, interrupt in self.interrupts.items():
            at_minute = interrupt["at_minute"]
            if at_minute <= elapsed_minutes < at_minute + 1:
                if name not in self.triggered_interrupts:
                    self.triggered_interrupts.add(name)
                    self.session_log["interrupts_shown"].append({
                        "name": name,
                        "at_minute": at_minute,
                        "message": interrupt["message"]
                    })
                    return interrupt["message"]
        return None
    
    def format_time(self, seconds: int) -> str:
        """Format seconds as MM:SS."""
        mins, secs = divmod(abs(int(seconds)), 60)
        sign = "-" if seconds < 0 else ""
        return f"{sign}{mins:02d}:{secs:02d}"
    
    def run_with_rich(self):
        """Run timer with rich console UI."""
        self.start_time = time.time()
        self.session_log["start_time"] = datetime.now().isoformat()
        
        self.console.clear()
        self.console.print(Panel(
            f"[bold cyan]{self.problem_name}[/]\n\n"
            f"Total time: {self.format_time(self.total_duration)}\n"
            f"Stages: {len(self.stages)}",
            title="🎯 Interview Timer Starting",
            border_style="cyan"
        ))
        time.sleep(2)
        
        last_stage_idx = -1
        
        try:
            while True:
                elapsed = int(time.time() - self.start_time)
                elapsed_minutes = elapsed // 60
                remaining = self.total_duration - elapsed
                
                stage_idx, stage, stage_elapsed, stage_remaining = self.get_current_stage(elapsed)
                
                # Stage transition
                if stage_idx != last_stage_idx:
                    if last_stage_idx >= 0:
                        self.session_log["stages"].append({
                            "name": self.stages[last_stage_idx]["name"],
                            "completed_at": elapsed
                        })
                    
                    last_stage_idx = stage_idx
                    if self.audio_enabled:
                        play_alert("stage")
                    
                    self.console.clear()
                    self.console.print(Panel(
                        f"[bold yellow]{stage['name']}[/]\n\n"
                        f"[dim]{stage['prompt']}[/]",
                        title=f"Stage {stage_idx + 1}/{len(self.stages)}",
                        border_style="yellow"
                    ))
                    time.sleep(1)
                
                # Check interrupts
                interrupt_msg = self.check_interrupts(elapsed_minutes)
                if interrupt_msg:
                    if self.audio_enabled:
                        play_alert("interrupt")
                    self.console.print(Panel(
                        f"[bold red]{interrupt_msg}[/]",
                        title="⚠️  INTERRUPT",
                        border_style="red"
                    ))
                    time.sleep(3)
                
                # Display timer
                self.console.clear()
                
                # Build display
                stage_progress = (stage_elapsed / (stage["duration_minutes"] * 60)) * 100
                overall_progress = (elapsed / self.total_duration) * 100
                
                table = Table(show_header=False, box=None, padding=(0, 2))
                table.add_column(justify="right", style="dim")
                table.add_column(justify="left")
                
                table.add_row("Problem:", f"[bold]{self.problem_name}[/]")
                table.add_row("Stage:", f"[yellow]{stage['name']}[/] ({stage_idx + 1}/{len(self.stages)})")
                table.add_row("Stage Time:", f"[cyan]{self.format_time(stage_remaining)}[/] remaining")
                table.add_row("Total Time:", f"[{'green' if remaining > 300 else 'red'}]{self.format_time(remaining)}[/] remaining")
                table.add_row("", "")
                table.add_row("Prompt:", f"[dim italic]{stage['prompt']}[/]")
                
                self.console.print(Panel(table, title="🎯 Interview Timer", border_style="cyan"))
                
                # Progress bars
                self.console.print(f"\nStage Progress:  [{'█' * int(stage_progress // 5)}{'░' * (20 - int(stage_progress // 5))}] {stage_progress:.0f}%")
                self.console.print(f"Overall Progress: [{'█' * int(overall_progress // 5)}{'░' * (20 - int(overall_progress // 5))}] {overall_progress:.0f}%")
                
                self.console.print("\n[dim]Press Ctrl+C to end session[/]")
                
                if remaining <= 0:
                    self.console.print(Panel(
                        "[bold red]TIME'S UP![/]\n\n"
                        "Wrap up your solution and prepare for postmortem.",
                        title="⏰ Session Complete",
                        border_style="red"
                    ))
                    if self.audio_enabled:
                        for _ in range(3):
                            play_alert("interrupt")
                            time.sleep(0.3)
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Session ended early.[/]")
        
        self.session_log["end_time"] = datetime.now().isoformat()
        self.save_session_log()
        
        return self.session_log
    
    def run_simple(self):
        """Run timer with simple console output (no rich)."""
        self.start_time = time.time()
        self.session_log["start_time"] = datetime.now().isoformat()
        
        print(f"\n{'='*50}")
        print(f"INTERVIEW TIMER: {self.problem_name}")
        print(f"Total time: {self.format_time(self.total_duration)}")
        print(f"{'='*50}\n")
        
        last_stage_idx = -1
        
        try:
            while True:
                elapsed = int(time.time() - self.start_time)
                elapsed_minutes = elapsed // 60
                remaining = self.total_duration - elapsed
                
                stage_idx, stage, stage_elapsed, stage_remaining = self.get_current_stage(elapsed)
                
                if stage_idx != last_stage_idx:
                    last_stage_idx = stage_idx
                    print(f"\n>>> STAGE {stage_idx + 1}: {stage['name']}")
                    print(f"    {stage['prompt']}\n")
                
                interrupt_msg = self.check_interrupts(elapsed_minutes)
                if interrupt_msg:
                    print(f"\n!!! {interrupt_msg} !!!\n")
                
                sys.stdout.write(f"\rTotal: {self.format_time(remaining)} | Stage: {self.format_time(stage_remaining)}    ")
                sys.stdout.flush()
                
                if remaining <= 0:
                    print("\n\n>>> TIME'S UP! <<<\n")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nSession ended early.")
        
        self.session_log["end_time"] = datetime.now().isoformat()
        self.save_session_log()
        
        return self.session_log
    
    def run(self):
        """Run the timer with best available UI."""
        if RICH_AVAILABLE and self.console:
            return self.run_with_rich()
        else:
            return self.run_simple()
    
    def save_session_log(self):
        """Save session log to file."""
        logs_dir = Path(__file__).parent.parent / "logs" / "sessions"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_problem = self.problem_name.replace("/", "_").replace(" ", "_")
        filename = f"{timestamp}_{safe_problem}.json"
        
        with open(logs_dir / filename, "w") as f:
            json.dump(self.session_log, f, indent=2)
        
        print(f"\nSession saved to: logs/sessions/{filename}")


# =============================================================================
# PROBLEM LOADING
# =============================================================================

def load_problem(problem_path: str) -> Dict:
    """Load problem from the problem bank."""
    base_dir = Path(__file__).parent.parent / "problems"
    problem_dir = base_dir / problem_path
    
    if not problem_dir.exists():
        return {"name": problem_path, "statement": "Problem not found."}
    
    problem_file = problem_dir / "problem.md"
    if problem_file.exists():
        with open(problem_file) as f:
            content = f.read()
        
        # Extract title from first line
        lines = content.strip().split("\n")
        title = lines[0].lstrip("#").strip() if lines else problem_path
        
        return {
            "name": title,
            "path": str(problem_dir),
            "statement": content
        }
    
    return {"name": problem_path, "statement": ""}


def get_problem_for_day(day: int) -> Optional[str]:
    """Get the problem path for a given sprint day."""
    schedule_file = Path(__file__).parent.parent / "sprint" / "schedule.yaml"
    
    if schedule_file.exists():
        with open(schedule_file) as f:
            schedule = yaml.safe_load(f)
        
        days = schedule.get("days", [])
        if 0 < day <= len(days):
            return days[day - 1].get("problem")
    
    return None


# =============================================================================
# CLI COMMANDS
# =============================================================================

@click.command()
@click.option("--day", "-d", type=int, help="Sprint day number (1-14)")
@click.option("--problem", "-p", type=str, help="Problem path (e.g., hashmap/problem_01)")
@click.option("--duration", "-t", type=int, help="Override duration in minutes")
@click.option("--no-audio", is_flag=True, help="Disable audio alerts")
def main(day: Optional[int], problem: Optional[str], duration: Optional[int], no_audio: bool):
    """
    Start a timed interview practice session.
    
    Examples:
        python -m cli.timer --day 1
        python -m cli.timer --problem hashmap/problem_01_group_anagrams
        python -m cli.timer --duration 30
    """
    config = load_config()
    
    # Determine problem
    problem_name = "Practice Problem"
    
    if day:
        problem_path = get_problem_for_day(day)
        if problem_path:
            problem_info = load_problem(problem_path)
            problem_name = problem_info["name"]
        else:
            problem_name = f"Day {day} Problem"
    elif problem:
        problem_info = load_problem(problem)
        problem_name = problem_info.get("name", problem)
    
    # Override settings
    if duration:
        # Adjust stage durations proportionally
        total_default = sum(s["duration_minutes"] for s in config["timer"]["stages"])
        ratio = duration / total_default
        for stage in config["timer"]["stages"]:
            stage["duration_minutes"] = max(1, int(stage["duration_minutes"] * ratio))
    
    if no_audio:
        config["timer"]["audio_enabled"] = False
    
    # Run timer
    timer = InterviewTimer(config, problem_name)
    
    console = Console() if RICH_AVAILABLE else None
    if console:
        console.print(Panel(
            "[bold]Interview Timer Ready[/]\n\n"
            f"Problem: [cyan]{problem_name}[/]\n"
            f"Duration: [yellow]{sum(s['duration_minutes'] for s in config['timer']['stages'])} minutes[/]\n\n"
            "[dim]Press Enter to start, Ctrl+C to cancel[/]",
            title="🎯 FRS Interview Sprint",
            border_style="green"
        ))
    else:
        print(f"\nReady to start: {problem_name}")
        print("Press Enter to start, Ctrl+C to cancel")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nCancelled.")
        return
    
    session = timer.run()
    
    # Prompt for postmortem
    if console:
        console.print("\n[bold yellow]Don't forget to record your postmortem![/]")
        console.print("[dim]Run: python -m cli.postmortem[/]\n")
    else:
        print("\nDon't forget to record your postmortem!")
        print("Run: python -m cli.postmortem\n")


if __name__ == "__main__":
    main()

