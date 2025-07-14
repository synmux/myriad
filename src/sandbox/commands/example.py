"""
Example command for Sandbox CLI

A minimal example command demonstrating the basic command structure.
"""

import click
from typing_extensions import override

from ..command_interface import BaseCommand, GlobalConfig
from ..util import console


class ExampleCommand(BaseCommand):
    """Minimal example command"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the example command with the CLI group"""

        @cli_group.command()
        @click.pass_context
        def example(ctx: click.Context) -> None:  # type: ignore
            """
            📝 A minimal example command

            This is a simple example demonstrating the basic command structure.
            """
            config = ExampleCommand.get_config_from_context(ctx)
            ExampleCommand.execute(config)

    @staticmethod
    def execute(config: GlobalConfig) -> None:
        """
        Execute the example command

        Args:
            config: Global configuration object
        """
        if ExampleCommand.should_skip_output(config):
            return

        console.print("Hello from the example command! 👋")

        if config.verbose:
            console.print("Verbose mode is enabled.")

        if config.debug:
            console.print("Debug mode is enabled.")
