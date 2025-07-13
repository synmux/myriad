"""
Hello command for Sandbox CLI

A spectacular hello world command that demonstrates rainbow animations,
fancy panels, and all the visual capabilities of the CLI tool.
"""

import time
from typing import Any, Dict, List

import click

from ..command_interface import BaseCommand, GlobalConfig
from ..utils import (
    console,
    create_fancy_panel,
    output_data,
    show_welcome_animation,
    show_completion_animation,
    print_debug_info,
)


class HelloCommand(BaseCommand):
    """Hello world command with spectacular animations"""

    @staticmethod
    def register_command(cli_group: click.Group) -> None:
        """Register the hello command with the CLI group"""

        @cli_group.command()
        @click.pass_context
        def hello(ctx: click.Context) -> None:
            """
            🎉 A spectacular hello world with rainbow animations!

            This command demonstrates all the visual capabilities of the CLI tool
            with colorful animations, spinners, and fancy panels.
            """
            config = HelloCommand.get_config_from_context(ctx)
            HelloCommand.execute(config)

    @staticmethod
    def execute(config: GlobalConfig) -> None:
        """
        Execute the hello command

        Args:
            config: Global configuration object
        """
        if HelloCommand.should_skip_output(config):
            return

        # Print debug info if enabled
        print_debug_info(config, {"command": "hello"})

        # Welcome animation
        show_welcome_animation("rainbow magic", config)

        # Main greeting
        greeting_panel = create_fancy_panel(
            "🌈 HELLO WORLD 🌈",
            "Welcome to the most spectacular CLI tool ever created!",
            config
        )
        console.print(greeting_panel)

        if not config.quiet:
            console.print()
            from ..utils import animate_spinner_with_text
            animate_spinner_with_text("Generating awesome data...", 1.0)

        # Sample data output
        sample_data = HelloCommand._generate_sample_data(config)
        output_data(sample_data, config)

        # Closing animation
        if not config.quiet:
            console.print()
            from ..utils import animate_spinner_with_text
            animate_spinner_with_text("Wrapping up the magic...", 1.0)

            farewell_panel = create_fancy_panel(
                "✨ GOODBYE ✨",
                "Thanks for trying our rainbow CLI tool!",
                config
            )
            console.print(farewell_panel)

    @staticmethod
    def _generate_sample_data(config: GlobalConfig) -> Dict[str, Any]:
        """
        Generate sample data for the hello command

        Args:
            config: Global configuration object

        Returns:
            Dict[str, Any]: Sample data dictionary
        """
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
                "cli_features": "All the bells and whistles activated!",
                "command_info": {
                    "name": "hello",
                    "description": "Spectacular hello world with animations",
                    "features_demonstrated": [
                        "Rainbow text rendering",
                        "Fancy panels with borders",
                        "Spinner animations",
                        "Multiple output formats",
                        "Global flag integration"
                    ]
                }
            }

        return sample_data
