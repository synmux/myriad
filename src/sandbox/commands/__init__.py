"""
Commands package for Sandbox CLI

This package contains all the individual command modules that are auto-loaded
by the CLI. Each command module should contain a class that implements the
CommandProtocol and provides a register_command static method.
"""

# This file makes the commands directory a Python package
# Individual command modules are auto-discovered and loaded by the CommandRegistry
