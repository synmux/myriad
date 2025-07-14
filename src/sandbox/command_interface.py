"""
Command interface and utilities for the Sandbox CLI

This module provides the base interface that all commands should implement,
along with utilities for auto-loading commands from the commands/ directory.
"""

import importlib
import inspect
import pkgutil
import types
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

import click
from pydantic import BaseModel


class GlobalConfig(BaseModel):
    """Global configuration for the CLI"""

    verbose: bool = False
    debug: bool = False
    quiet: bool = False
    silent: bool = False
    output_format: str = "normal"


class CommandProtocol(Protocol):
    """Protocol that all command classes should implement"""

    @staticmethod
    def register_command(cli_group: click.Group) -> None:
        """Register this command with the CLI group"""
        ...


class BaseCommand(ABC):
    """
    Abstract base class for CLI commands

    All commands should inherit from this class and implement the required methods.
    This provides a consistent interface and helpful utilities.
    """

    @staticmethod
    @abstractmethod
    def register_command(cli_group: click.Group) -> None:
        """
        Register this command with the CLI group

        This method should define the click command and add it to the group.
        It should include all command-specific options and the command function.

        Args:
            cli_group: The main CLI group to register the command with
        """
        pass

    @staticmethod
    def get_config_from_context(ctx: click.Context) -> GlobalConfig:
        """
        Helper method to extract global config from click context

        Args:
            ctx: Click context object

        Returns:
            GlobalConfig: The global configuration object
        """
        config: GlobalConfig = ctx.obj["config"]
        return config

    @staticmethod
    def should_skip_output(config: GlobalConfig) -> bool:
        """
        Check if output should be skipped based on config

        Args:
            config: Global configuration

        Returns:
            bool: True if output should be skipped (silent mode)
        """
        return config.silent


class CommandRegistry:
    """Registry for managing command auto-loading and registration"""

    def __init__(self, commands_package: str = "sandbox.commands"):
        """
        Initialize the command registry

        Args:
            commands_package: Package name where commands are located
        """
        self.commands_package: str = commands_package
        self.registered_commands: list[type[CommandProtocol]] = []

    def discover_commands(self) -> list[type[CommandProtocol]]:
        """
        Discover all command classes in the commands package

        Returns:
            list[type[CommandProtocol]]: List of discovered command classes
        """
        commands: list[type[CommandProtocol]] = []

        try:
            # Import the commands package
            commands_module = importlib.import_module(self.commands_package)

            # Get the package path
            package_path: list[str]
            if hasattr(commands_module, "__path__"):
                package_path = list(commands_module.__path__)
            else:
                # Fallback for namespace packages
                module_file = commands_module.__file__
                if module_file is not None:
                    package_path = [str(Path(module_file).parent)]
                else:
                    # Cannot determine package path, skip discovery
                    return commands

            # Iterate through all modules in the package
            for _, module_name, ispkg in pkgutil.iter_modules(package_path):
                if not ispkg and not module_name.startswith("_"):
                    full_module_name = f"{self.commands_package}.{module_name}"

                    try:
                        module: types.ModuleType = importlib.import_module(
                            full_module_name
                        )

                        # Find all classes that implement CommandProtocol
                        commands.extend(
                            [
                                obj
                                for name, obj in inspect.getmembers(
                                    module, inspect.isclass
                                )
                                if (
                                    hasattr(obj, "register_command")
                                    and callable(obj.register_command)
                                    and obj != BaseCommand
                                    and not name.startswith("_")
                                )
                            ]
                        )

                    except ImportError as e:
                        print(
                            f"Warning: Could not import command module {full_module_name}: {e}"
                        )

        except ImportError as e:
            print(
                f"Warning: Could not import commands package {self.commands_package}: {e}"
            )

        self.registered_commands = commands
        return commands

    def register_all_commands(self, cli_group: click.Group) -> None:
        """
        Register all discovered commands with the CLI group

        Args:
            cli_group: The main CLI group to register commands with
        """
        commands = self.discover_commands()

        for command_class in commands:
            try:
                command_class.register_command(cli_group)
            except Exception as e:
                print(
                    f"Warning: Could not register command {command_class.__name__}: {e}"
                )

    def get_registered_commands(self) -> list[type[CommandProtocol]]:
        """
        Get list of registered command classes

        Returns:
            list[type[CommandProtocol]]: List of registered commands
        """
        return self.registered_commands.copy()


def create_command_registry(
    commands_package: str = "sandbox.commands",
) -> CommandRegistry:
    """
    Factory function to create a command registry

    Args:
        commands_package: Package name where commands are located

    Returns:
        CommandRegistry: Configured command registry
    """
    return CommandRegistry(commands_package)
