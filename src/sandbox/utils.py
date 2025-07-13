"""
Shared utilities for Sandbox CLI commands

This module contains common functionality used across multiple commands,
including output formatting, animations, and Rich UI components.
"""

import json
import time
from enum import Enum
from typing import Any

import yaml
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from .command_interface import GlobalConfig


class OutputFormat(str, Enum):
    """Output format options"""

    NORMAL = "normal"
    JSON = "json"
    YAML = "yaml"


# Global console instance
console = Console()


def create_rainbow_text(text: str) -> Text:
    """
    Create rainbow colored text

    Args:
        text: The text to colorize

    Returns:
        Text: Rich Text object with rainbow colors
    """
    colors = ["red", "orange3", "yellow", "green", "blue", "purple", "magenta"]
    rainbow_text = Text()

    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        _ = rainbow_text.append(char, style=color)

    return rainbow_text


def animate_spinner_with_text(text: str, duration: float = 2.0) -> None:
    """
    Animate a spinner with colorful text

    Args:
        text: Text to display with the spinner
        duration: How long to show the spinner (seconds)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(description=text, total=None)
        time.sleep(duration)
        progress.remove_task(task)


def create_fancy_panel(title: str, content: str, config: GlobalConfig) -> Panel:
    """
    Create a fancy panel with the given content

    Args:
        title: Panel title
        content: Panel content
        config: Global configuration

    Returns:
        Panel: Rich Panel object with styling
    """
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


def output_data(data: dict[str, Any], config: GlobalConfig) -> None:
    """
    Output data in the specified format

    Args:
        data: Data dictionary to output
        config: Global configuration determining output format
    """
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


def create_data_table(
    title: str, columns: dict[str, str], rows: list[list[str]], max_rows: int = 10
) -> Table:
    """
    Create a Rich table with the given data

    Args:
        title: Table title
        columns: Dictionary of column names to styles
        rows: List of row data
        max_rows: Maximum number of rows to display

    Returns:
        Table: Rich Table object
    """
    table = Table(
        title=create_rainbow_text(title),
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )

    # Add columns
    for column_name, style in columns.items():
        table.add_column(column_name, style=style)

    # Add rows (limited to max_rows)
    for row in rows[:max_rows]:
        table.add_row(*[str(cell) for cell in row])

    # Add ellipsis if there are more rows
    if len(rows) > max_rows:
        ellipsis_row = ["..."] * len(columns)
        table.add_row(*ellipsis_row, style="dim")

    return table


def show_welcome_animation(message: str, config: GlobalConfig) -> None:
    """
    Show a welcome animation if not in quiet mode

    Args:
        message: Welcome message to display
        config: Global configuration
    """
    if config.quiet or config.silent:
        return

    animate_spinner_with_text(f"Initializing {message}...", 1.5)
    console.print()


def show_completion_animation(message: str, config: GlobalConfig) -> None:
    """
    Show a completion animation if not in quiet mode

    Args:
        message: Completion message to display
        config: Global configuration
    """
    if config.quiet or config.silent:
        return

    console.print()
    animate_spinner_with_text(f"Wrapping up {message}...", 1.0)


def print_debug_info(
    config: GlobalConfig, extra_info: dict[str, Any] | None = None
) -> None:
    """
    Print debug information if debug mode is enabled

    Args:
        config: Global configuration
        extra_info: Additional debug information to display
    """
    if not config.debug or config.silent:
        return

    debug_data: dict[str, Any] = {"config": config.model_dump()}
    if extra_info:
        debug_data.update(extra_info)

    console.print(f"[dim]Debug info: {debug_data}[/dim]")


def get_output_format_from_config(config: GlobalConfig) -> OutputFormat:
    """
    Get the OutputFormat enum value from config

    Args:
        config: Global configuration

    Returns:
        OutputFormat: The output format enum value
    """
    try:
        return OutputFormat(config.output_format)
    except ValueError:
        return OutputFormat.NORMAL
