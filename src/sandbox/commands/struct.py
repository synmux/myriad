"""
Struct command for Sandbox CLI

Test structured replies from OpenRouter
"""

import click
from typing_extensions import override

from ..command_interface import BaseCommand, GlobalConfig
from ..util import console
from ..util.ai import get_openai_client


class StructCommand(BaseCommand):
    """Minimal struct command"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the struct command with the CLI group"""

        @cli_group.command()
        @click.pass_context
        def struct(ctx: click.Context) -> None:  # type: ignore
            """
            📝 A minimal struct command

            This is a simple struct demonstrating the basic command structure.
            """
            config = StructCommand.get_config_from_context(ctx)
            StructCommand.execute(config)

    @staticmethod
    def execute(config: GlobalConfig) -> None:
        """
        Execute the struct command

        Args:
            config: Global configuration object
        """
        if StructCommand.should_skip_output(config):
            return

        # CODE BEGINS HERE

        client = get_openai_client(enable_caching=False)

        print(client.__repr__())

        if config.verbose:
            console.print("Verbose mode is enabled.")

        if config.debug:
            console.print("Debug mode is enabled.")
