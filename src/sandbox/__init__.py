"""
Sandbox CLI - A fun command-line tool with animated output
"""

import json
import time
from enum import Enum
from typing import Any, Dict, Optional

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from rich import box
from pydantic import BaseModel


class OutputFormat(str, Enum):
    """Output format options"""
    NORMAL = "normal"
    JSON = "json"
    YAML = "yaml"


class GlobalConfig(BaseModel):
    """Global configuration for the CLI"""
    verbose: bool = False
    debug: bool = False
    quiet: bool = False
    silent: bool = False
    output_format: OutputFormat = OutputFormat.NORMAL


# Global console instance
console = Console()


def create_rainbow_text(text: str) -> Text:
    """Create rainbow colored text"""
    colors = ["red", "orange3", "yellow", "green", "blue", "purple", "magenta"]
    rainbow_text = Text()

    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow_text.append(char, style=color)

    return rainbow_text


def animate_spinner_with_text(text: str, duration: float = 2.0) -> None:
    """Animate a spinner with colorful text"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(description=create_rainbow_text(text), total=None)
        time.sleep(duration)
        progress.remove_task(task)


def create_fancy_panel(title: str, content: str, config: GlobalConfig) -> Panel:
    """Create a fancy panel with the given content"""
    if config.silent:
        return Panel("")

    rainbow_title = create_rainbow_text(title)
    rainbow_content = create_rainbow_text(content)

    return Panel(
        Align.center(rainbow_content),
        title=rainbow_title,
        box=box.DOUBLE,
        border_style="bright_cyan",
        padding=(1, 2),
    )


def output_data(data: Dict[str, Any], config: GlobalConfig) -> None:
    """Output data in the specified format"""
    if config.silent:
        return

    if config.output_format == OutputFormat.JSON:
        console.print(json.dumps(data, indent=2))
    elif config.output_format == OutputFormat.YAML:
        console.print(yaml.dump(data, default_flow_style=False))
    else:
        # Normal rich output
        table = Table(title=create_rainbow_text("Output Data"), box=box.ROUNDED)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        console.print(table)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--json', '-j', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('--yaml', '-y', 'output_yaml', is_flag=True, help='Output in YAML format')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.option('--quiet', '-q', is_flag=True, help='Suppress normal output')
@click.option('--silent', '-s', is_flag=True, help='Suppress all output')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, output_json: bool, output_yaml: bool,
        debug: bool, quiet: bool, silent: bool) -> None:
    """
    🌈 Sandbox CLI - A delightfully animated command-line tool

    A fun CLI tool that demonstrates colorful animations and various output formats.
    """
    # Determine output format
    output_format = OutputFormat.NORMAL
    if output_json:
        output_format = OutputFormat.JSON
    elif output_yaml:
        output_format = OutputFormat.YAML

    # Create global config
    config = GlobalConfig(
        verbose=verbose,
        debug=debug,
        quiet=quiet,
        silent=silent,
        output_format=output_format
    )

    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = config

    if debug and not silent:
        console.print(f"[dim]Debug mode enabled[/dim]")
        console.print(f"[dim]Config: {config.model_dump()}[/dim]")


@cli.command()
@click.pass_context
def hello(ctx: click.Context) -> None:
    """
    🎉 A spectacular hello world with rainbow animations!

    This command demonstrates all the visual capabilities of the CLI tool
    with colorful animations, spinners, and fancy panels.
    """
    config: GlobalConfig = ctx.obj['config']

    if config.silent:
        return

    # Welcome animation
    if not config.quiet:
        animate_spinner_with_text("Initializing rainbow magic...", 1.5)
        console.print()

    # Main greeting
    greeting_panel = create_fancy_panel(
        "🌈 HELLO WORLD 🌈",
        "Welcome to the most spectacular CLI tool ever created!",
        config
    )
    console.print(greeting_panel)

    if not config.quiet:
        console.print()
        animate_spinner_with_text("Generating awesome data...", 1.0)

    # Sample data output
    sample_data = {
        "message": "Hello from the sandbox!",
        "timestamp": time.time(),
        "version": "0.1.0",
        "features": ["rainbow colors", "animations", "multiple formats"],
        "mood": "absolutely fantastic! 🎉"
    }

    if config.verbose:
        sample_data["verbose_info"] = {
            "config": config.model_dump(),
            "cli_features": "All the bells and whistles activated!"
        }

    output_data(sample_data, config)

    # Closing animation
    if not config.quiet:
        console.print()
        animate_spinner_with_text("Wrapping up the magic...", 1.0)

        farewell_panel = create_fancy_panel(
            "✨ GOODBYE ✨",
            "Thanks for trying our rainbow CLI tool!",
            config
        )
        console.print(farewell_panel)


@cli.command()
@click.option('--count', '-c', default=5, help='Number of demo items to process')
@click.option('--speed', '-s', default=0.1, help='Animation speed (seconds per step)')
@click.pass_context
def demo(ctx: click.Context, count: int, speed: float) -> None:
    """
    🚀 Advanced demo showcasing progress bars, tables, and more animations!

    This command demonstrates advanced CLI features including:
    - Progress bars with multiple tasks
    - Dynamic tables
    - Animated ASCII art
    - Complex data structures
    """
    config: GlobalConfig = ctx.obj['config']

    if config.silent:
        return

    # Animated ASCII art banner
    if not config.quiet:
        banner_lines = [
            "  ██████  ▄▄▄       ███▄    █ ▓█████▄  ▄▄▄▄    ▒█████  ▒██   ██▒",
            "▒██    ▒ ▒████▄     ██ ▀█   █ ▒██▀ ██▌▓█████▄ ▒██▒  ██▒▒▒ █ █ ▒░",
            "░ ▓██▄   ▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▌▒██▒ ▄██▒██░  ██▒░░  █   ░",
            "  ▒   ██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌▒██░█▀  ▒██   ██░ ░ █ █ ▒ ",
            "▒██████▒▒ ▓█   ▓██▒▒██░   ▓██░░▒████▓ ░▓█  ▀█▓░ ████▓▒░▒██▒ ▒██▒",
            "▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒ ░▒▓███▀▒░ ▒░▒░▒░ ▒▒ ░ ░▓ ░",
            "░ ░▒  ░ ░  ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒ ▒░▒   ░   ░ ▒ ▒░ ░░   ░▒ ░",
        ]

        for line in banner_lines:
            rainbow_line = create_rainbow_text(line)
            console.print(Align.center(rainbow_line))
            time.sleep(speed)

        console.print()

    # Progress bar demo
    if not config.quiet:
        animate_spinner_with_text("Starting advanced demo...", 1.0)

    demo_data = []

    with Progress(console=console) as progress:
        main_task = progress.add_task("[green]Processing demo items...", total=count)
        data_task = progress.add_task("[blue]Generating data...", total=count)

        for i in range(count):
            # Simulate some work
            time.sleep(speed)

            # Generate demo data
            item_data = {
                "id": f"item_{i+1:03d}",
                "name": f"Demo Item {i+1}",
                "status": "✅ Complete" if i % 2 == 0 else "🔄 Processing",
                "score": round((i + 1) * 20.5, 2),
                "category": ["Alpha", "Beta", "Gamma", "Delta"][i % 4]
            }
            demo_data.append(item_data)

            progress.update(main_task, advance=1)
            progress.update(data_task, advance=1)

    # Create output data structure
    output_data_structure = {
        "demo_summary": {
            "total_items": count,
            "processing_speed": speed,
            "timestamp": time.time(),
            "features_demonstrated": [
                "ASCII art animation",
                "Multi-task progress bars",
                "Dynamic data generation",
                "Rich table formatting"
            ]
        },
        "items": demo_data,
        "statistics": {
            "avg_score": sum(item["score"] for item in demo_data) / len(demo_data),
            "completed_items": len([item for item in demo_data if "Complete" in item["status"]]),
            "categories": list(set(item["category"] for item in demo_data))
        }
    }

    if config.verbose:
        output_data_structure["verbose_details"] = {
            "config": config.model_dump(),
            "command_options": {"count": count, "speed": speed},
            "rich_features_used": ["Progress", "Table", "Panel", "Text", "Align"]
        }

    # Output the data
    output_data(output_data_structure, config)

    # Show a fancy table if in normal mode
    if config.output_format == OutputFormat.NORMAL and not config.quiet:
        console.print()

        items_table = Table(
            title=create_rainbow_text("🎯 Demo Items Summary"),
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        items_table.add_column("ID", style="dim", width=12)
        items_table.add_column("Name", style="bold")
        items_table.add_column("Status", justify="center")
        items_table.add_column("Score", justify="right", style="yellow")
        items_table.add_column("Category", style="green")

        for item in demo_data[:min(10, len(demo_data))]:  # Show max 10 items
            items_table.add_row(
                item["id"],
                item["name"],
                item["status"],
                str(item["score"]),
                item["category"]
            )

        if len(demo_data) > 10:
            items_table.add_row("...", "...", "...", "...", "...", style="dim")

        console.print(items_table)

    # Final flourish
    if not config.quiet:
        console.print()
        animate_spinner_with_text("Demo complete! ✨", 1.0)

        completion_panel = create_fancy_panel(
            "🎉 DEMO COMPLETE 🎉",
            f"Successfully processed {count} items with {len(set(item['category'] for item in demo_data))} categories!",
            config
        )
        console.print(completion_panel)


def main() -> None:
    """Main entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
