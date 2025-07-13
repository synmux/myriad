"""
Sandbox CLI - A fun command-line tool with animated output

This is the main entry point for the Sandbox CLI tool. It sets up the global
configuration, auto-loads commands from the commands/ directory, and provides
a consistent interface across all subcommands.
"""

import click
from rich.console import Console

from .command_interface import GlobalConfig, create_command_registry
from .utils import OutputFormat

# Global console instance
console = Console()


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--json", "-j", "output_json", is_flag=True, help="Output in JSON format")
@click.option("--yaml", "-y", "output_yaml", is_flag=True, help="Output in YAML format")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option("--quiet", "-q", is_flag=True, help="Suppress normal output")
@click.option("--silent", "-s", is_flag=True, help="Suppress all output")
@click.pass_context
def cli(
    ctx: click.Context,
    verbose: bool,
    output_json: bool,
    output_yaml: bool,
    debug: bool,
    quiet: bool,
    silent: bool,
) -> None:
    """
    🌈 Sandbox CLI - A delightfully animated command-line tool

    A fun CLI tool that demonstrates colorful animations and various output formats.
    Features modular command architecture with auto-loading from the commands/ directory.
    """
    # Determine output format
    output_format = OutputFormat.NORMAL.value
    if output_json:
        output_format = OutputFormat.JSON.value
    elif output_yaml:
        output_format = OutputFormat.YAML.value

    # Create global config
    config = GlobalConfig(
        verbose=verbose,
        debug=debug,
        quiet=quiet,
        silent=silent,
        output_format=output_format,
    )

    # Store config in context
    _ = ctx.ensure_object(dict)
    ctx.obj["config"] = config

    if debug and not silent:
        console.print("[dim]Debug mode enabled[/dim]")
        console.print(f"[dim]Config: {config.model_dump()}[/dim]")


def main() -> None:
    """Main entry point for the CLI"""
    # Create command registry and auto-load all commands
    registry = create_command_registry("sandbox.commands")
    registry.register_all_commands(cli)

    # Run the CLI
    cli()


if __name__ == "__main__":
    main()
