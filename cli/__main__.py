"""
CLI entry point for the Interview Sprint Platform.

Usage:
    python -m cli timer --day 1
    python -m cli mock
    python -m cli postmortem
    python -m cli progress
"""

import click


@click.group()
def cli():
    """FRS Interview Sprint Platform CLI"""
    pass


@cli.command()
@click.option("--day", "-d", type=int, help="Sprint day number (1-14)")
@click.option("--problem", "-p", type=str, help="Problem path")
@click.option("--duration", "-t", type=int, help="Duration in minutes")
@click.option("--no-audio", is_flag=True, help="Disable audio")
def timer(day, problem, duration, no_audio):
    """Start a timed coding session."""
    from cli.timer import main as timer_main
    # Call the main function directly with arguments
    timer_main(day=day, problem=problem, duration=duration, no_audio=no_audio)


@cli.command()
@click.option("--duration", "-t", type=int, default=35, help="Duration in minutes")
@click.option("--pattern", "-p", type=str, help="Specific pattern to practice")
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["core", "aie"]),
    default="core",
    show_default=True,
    help="Mock track to run",
)
@click.option("--list-problems", "-l", is_flag=True, help="List available problems")
def mock(duration, pattern, mode, list_problems):
    """Run a full mock interview."""
    from cli.mock import main as mock_main
    mock_main(duration=duration, pattern=pattern, mode=mode, list_problems=list_problems)


@cli.command()
@click.option("--problem", "-p", type=str, help="Problem name for postmortem")
@click.option("--view-last", "-v", is_flag=True, help="View last postmortem")
def postmortem(problem, view_last):
    """Record a postmortem for the last session."""
    from cli.postmortem import main as postmortem_main
    postmortem_main(problem=problem, view_last=view_last)


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Show detailed view")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def progress(detailed, as_json):
    """View the progress dashboard."""
    from cli.progress import main as progress_main
    progress_main(detailed=detailed, as_json=as_json)


if __name__ == "__main__":
    cli()

