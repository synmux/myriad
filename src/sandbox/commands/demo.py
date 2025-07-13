"""
Demo command for Sandbox CLI

An advanced demonstration showcasing progress bars, tables, ASCII art,
and complex data structures with animations.
"""

import time
from typing import Any, override

import click
from rich.progress import Progress
from rich.align import Align
from rich.table import Table

from ..command_interface import BaseCommand, GlobalConfig
from ..utils import (
    console,
    create_fancy_panel,
    create_rainbow_text,
    output_data,
    show_welcome_animation,
    print_debug_info,
    create_data_table,
    get_output_format_from_config,
    OutputFormat,
    animate_spinner_with_text,
)


class DemoCommand(BaseCommand):
    """Advanced demo command with progress bars and animations"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the demo command with the CLI group"""

        @cli_group.command()
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
            config = DemoCommand.get_config_from_context(ctx)
            DemoCommand.execute(config, count, speed)

    @staticmethod
    def execute(config: GlobalConfig, count: int, speed: float) -> None:
        """
        Execute the demo command

        Args:
            config: Global configuration object
            count: Number of demo items to process
            speed: Animation speed in seconds
        """
        if DemoCommand.should_skip_output(config):
            return

        # Print debug info if enabled
        print_debug_info(config, {
            "command": "demo",
            "options": {"count": count, "speed": speed}
        })

        # Animated ASCII art banner
        if not config.quiet:
            DemoCommand._show_ascii_banner(speed)
            console.print()

        # Progress bar demo
        show_welcome_animation("advanced demo", config)

        demo_data = DemoCommand._process_demo_items(count, speed)

        # Create output data structure
        output_data_structure = DemoCommand._create_output_structure(
            count, speed, demo_data, config
        )

        # Output the data
        output_data(output_data_structure, config)

        # Show a fancy table if in normal mode
        if get_output_format_from_config(config) == OutputFormat.NORMAL and not config.quiet:
            console.print()
            items_table = DemoCommand._create_items_table(demo_data)
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

    @staticmethod
    def _show_ascii_banner(speed: float) -> None:
        """Show animated ASCII art banner"""
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

    @staticmethod
    def _process_demo_items(count: int, speed: float) -> list[dict[str, Any]]:
        """Process demo items with progress bars"""
        demo_data: list[dict[str, Any]] = []

        with Progress(console=console) as progress:
            main_task = progress.add_task("[green]Processing demo items...", total=count)
            data_task = progress.add_task("[blue]Generating data...", total=count)

            for i in range(count):
                # Simulate some work
                time.sleep(speed)

                # Generate demo data
                item_data: dict[str, Any] = {
                    "id": f"item_{i+1:03d}",
                    "name": f"Demo Item {i+1}",
                    "status": "✅ Complete" if i % 2 == 0 else "🔄 Processing",
                    "score": round((i + 1) * 20.5, 2),
                    "category": ["Alpha", "Beta", "Gamma", "Delta"][i % 4]
                }
                demo_data.append(item_data)

                progress.update(main_task, advance=1)
                progress.update(data_task, advance=1)

        return demo_data

    @staticmethod
    def _create_output_structure(
        count: int,
        speed: float,
        demo_data: list[dict[str, Any]],
        config: GlobalConfig
    ) -> dict[str, Any]:
        """Create the output data structure"""
        output_data_structure: dict[str, Any] = {
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
            verbose_details: dict[str, Any] = {
                "config": config.model_dump(),
                "command_options": {"count": count, "speed": speed},
                "rich_features_used": ["Progress", "Table", "Panel", "Text", "Align"],
                "command_info": {
                    "name": "demo",
                    "description": "Advanced demo with progress bars and animations",
                    "features_demonstrated": [
                        "ASCII art banner animation",
                        "Multi-task progress tracking",
                        "Dynamic data generation",
                        "Statistical calculations",
                        "Rich table formatting",
                        "Complex data structures"
                    ]
                }
            }
            output_data_structure["verbose_details"] = verbose_details

        return output_data_structure

    @staticmethod
    def _create_items_table(demo_data: list[dict[str, Any]]) -> Table:
        """Create a Rich table showing demo items"""
        columns = {
            "ID": "dim",
            "Name": "bold",
            "Status": "",
            "Score": "yellow",
            "Category": "green"
        }

        rows: list[list[str]] = []
        for item in demo_data:
            rows.append([
                str(item["id"]),
                str(item["name"]),
                str(item["status"]),
                str(item["score"]),
                str(item["category"])
            ])

        return create_data_table("🎯 Demo Items Summary", columns, rows, max_rows=10)
