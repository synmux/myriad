"""
Example command for Sandbox CLI

A simple example demonstrating how to create new commands that integrate
with the auto-loading system and follow the established patterns.
"""

import time
from typing import Any

import click
from typing_extensions import override

from ..command_interface import BaseCommand, GlobalConfig
from ..utils import (
    animate_spinner_with_text,
    console,
    create_fancy_panel,
    create_rainbow_text,
    output_data,
    print_debug_info,
    show_completion_animation,
    show_welcome_animation,
)


class ExampleCommand(BaseCommand):
    """Example command demonstrating the command interface"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the example command with the CLI group"""

        @cli_group.command()
        @click.option("--name", "-n", default="World", help="Name to greet")
        @click.option(
            "--repeat", "-r", default=1, help="Number of times to repeat the greeting"
        )
        @click.option(
            "--style",
            "-st",
            type=click.Choice(["simple", "fancy", "animated"]),
            default="simple",
            help="Style of greeting to use",
        )
        @click.pass_context
        def example(ctx: click.Context, name: str, repeat: int, style: str) -> None:
            """
            📚 Example command demonstrating command creation patterns!

            This command shows how to create new commands that integrate with
            the auto-loading system. It demonstrates:
            - Command-specific options
            - Different output styles
            - Global configuration usage
            - Proper error handling
            """
            config = ExampleCommand.get_config_from_context(ctx)
            ExampleCommand.execute(config, name, repeat, style)

    @staticmethod
    def execute(config: GlobalConfig, name: str, repeat: int, style: str) -> None:
        """
        Execute the example command

        Args:
            config: Global configuration object
            name: Name to greet
            repeat: Number of times to repeat
            style: Style of greeting
        """
        if ExampleCommand.should_skip_output(config):
            return

        # Print debug info if enabled
        print_debug_info(
            config,
            {
                "command": "example",
                "options": {"name": name, "repeat": repeat, "style": style},
            },
        )

        # Welcome animation
        show_welcome_animation("example command", config)

        # Generate greetings based on style
        greetings = ExampleCommand._generate_greetings(name, repeat, style)

        # Display greetings
        ExampleCommand._display_greetings(greetings, style, config)

        # Create output data
        output_data_structure = ExampleCommand._create_output_data(
            name, repeat, style, greetings, config
        )

        # Output the data
        output_data(output_data_structure, config)

        # Completion animation
        show_completion_animation("example command", config)

    @staticmethod
    def _generate_greetings(name: str, repeat: int, style: str) -> list[dict[str, Any]]:
        """Generate greetings based on parameters"""
        greetings: list[dict[str, Any]] = []

        base_messages = [
            f"Hello, {name}!",
            f"Greetings, {name}!",
            f"Welcome, {name}!",
            f"Hi there, {name}!",
            f"Hey, {name}!",
        ]

        for i in range(repeat):
            if repeat == 1:
                message = base_messages[0]
            else:
                message = base_messages[i % len(base_messages)]

            greeting: dict[str, Any] = {
                "iteration": i + 1,
                "message": message,
                "style": style,
                "timestamp": time.time(),
            }
            greetings.append(greeting)

        return greetings

    @staticmethod
    def _display_greetings(
        greetings: list[dict[str, Any]], style: str, config: GlobalConfig
    ) -> None:
        """Display greetings according to the specified style"""
        if config.quiet or config.silent:
            return

        if style == "simple":
            for greeting in greetings:
                console.print(f"[bold green]{str(greeting['message'])}[/bold green]")

        elif style == "fancy":
            for i, greeting in enumerate(greetings):
                panel = create_fancy_panel(
                    f"✨ Greeting #{greeting['iteration']} ✨",
                    str(greeting["message"]),
                    config,
                )
                console.print(panel)
                if i < len(greetings) - 1:  # Don't sleep after the last one
                    time.sleep(0.5)

        elif style == "animated":
            for greeting in greetings:
                animate_spinner_with_text(
                    f"Preparing greeting #{greeting['iteration']}...", 0.8
                )
                rainbow_message = create_rainbow_text(str(greeting["message"]))
                console.print(f"[bold]🎉 {rainbow_message} 🎉[/bold]")
                console.print()

    @staticmethod
    def _create_output_data(
        name: str,
        repeat: int,
        style: str,
        greetings: list[dict[str, Any]],
        config: GlobalConfig,
    ) -> dict[str, Any]:
        """Create the output data structure"""
        output_data_structure: dict[str, Any] = {
            "command_summary": {
                "name": "example",
                "target_name": name,
                "repetitions": repeat,
                "style": style,
                "total_greetings": len(greetings),
                "execution_time": time.time(),
            },
            "greetings": greetings,
            "statistics": {
                "unique_messages": len(set(str(g["message"]) for g in greetings)),
                "avg_message_length": sum(len(str(g["message"])) for g in greetings)
                / len(greetings),
                "styles_available": ["simple", "fancy", "animated"],
            },
        }

        if config.verbose:
            verbose_details: dict[str, Any] = {
                "config": config.model_dump(),
                "command_options": {"name": name, "repeat": repeat, "style": style},
                "command_info": {
                    "description": "Example command for demonstration purposes",
                    "features_demonstrated": [
                        "Command-specific options",
                        "Multiple output styles",
                        "Conditional animations",
                        "Data structure generation",
                        "Error handling patterns",
                    ],
                    "patterns_used": [
                        "BaseCommand inheritance",
                        "Static method organization",
                        "Global config integration",
                        "Utility function usage",
                    ],
                },
            }
            output_data_structure["verbose_details"] = verbose_details

        return output_data_structure
