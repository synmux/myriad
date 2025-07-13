# CLAUDE.md - AI Assistant Project Context

## Project Overview

This is a Python-based CLI tool called "Sandbox" that demonstrates advanced terminal user interfaces with animations, rainbow colors, and multiple output formats. The project showcases modern Python CLI development patterns using `click`, `rich`, and `pydantic` with a **modular command architecture** that auto-loads commands from a dedicated directory structure.

## Project Structure

```plaintext
myriad/
├── src/sandbox/
│   ├── __init__.py              # Main CLI entry point with auto-loading
│   ├── command_interface.py     # Base command interface and registry system
│   ├── utils.py                 # Shared utilities for all commands
│   └── commands/                # Auto-loaded command modules
│       ├── __init__.py         # Commands package
│       ├── hello.py           # Hello world command
│       ├── demo.py            # Advanced demo command
│       └── example.py         # Example command template
├── pyproject.toml              # Python project configuration
├── uv.lock                     # Dependency lock file
├── README.md                   # User documentation
└── CLAUDE.md                   # This file - AI assistant context
```

## Key Technologies

- **Package Management**: `uv` (fast Python package manager)
- **CLI Framework**: `click` (command-line interface creation)
- **Terminal UI**: `rich` (rich text and beautiful formatting)
- **Data Validation**: `pydantic` (data validation and settings)
- **Type System**: Full type hints with `typing` and `typing-extensions`
- **Output Formats**: JSON, YAML, Rich tables/panels
- **Command Architecture**: Modular auto-loading system with protocols

## Architecture Patterns

### Modular Command System

- Commands auto-discovered from `commands/` directory
- Each command is a separate module with a class implementing `CommandProtocol`
- `CommandRegistry` handles discovery and registration
- No need to manually register commands in main CLI file

### Command Interface

- `BaseCommand` abstract class provides common functionality
- `CommandProtocol` defines the interface all commands must implement
- Static `register_command()` method for Click integration
- Consistent access to global configuration via context

### Global Configuration

- Uses `GlobalConfig` Pydantic model for consistent settings across all commands
- Configuration passed through Click context object
- Supports: verbose, debug, quiet, silent modes + output formats
- Type-safe configuration access with helper methods

### Shared Utilities

- `utils.py` contains common functions used across commands
- Output formatting, animations, Rich components
- Consistent styling and behavior patterns
- Respects global flags (quiet/silent) automatically

### Auto-Loading System

- `CommandRegistry` class discovers commands at runtime
- Uses `importlib` and `pkgutil` for dynamic module loading
- Supports Python packages and namespace packages
- Error handling for failed imports or registration

## Current Commands

### `hello` (`commands/hello.py`)

- Basic "hello world" with rainbow animations
- Demonstrates: panels, spinners, data output, all flags
- Shows sample data structure with timestamps and metadata
- Template for simple commands with rich output

### `demo` (`commands/demo.py`)

- Advanced demo with progress bars and ASCII art
- Options: `--count` (items to process), `--speed` (animation speed)
- Demonstrates: multi-task progress, tables, complex data structures
- Shows statistical calculations and summaries

### `example` (`commands/example.py`)

- Template command showing how to create new commands
- Options: `--name`, `--repeat`, `--style` (simple/fancy/animated)
- Demonstrates: command-specific options, multiple styles, patterns
- Educational example for developers adding new commands

## Development Patterns

### Adding New Commands

1. **Create new file** in `src/sandbox/commands/`
2. **Import required modules**:
   ```python
   import click
   from ..command_interface import BaseCommand, GlobalConfig
   from ..utils import console, output_data, print_debug_info
   ```
3. **Create command class** inheriting from `BaseCommand`
4. **Implement `register_command` static method**
5. **Define `execute` static method** with command logic
6. **Use utility functions** for consistent behavior
7. **Command automatically loads** on next CLI run

### Command Class Template

```python
class MyCommand(BaseCommand):
    """Command description"""

    @staticmethod
    def register_command(cli_group: click.Group) -> None:
        @cli_group.command()
        @click.option('--flag', help='Description')
        @click.pass_context
        def mycommand(ctx: click.Context, flag: str) -> None:
            """Command help text"""
            config = MyCommand.get_config_from_context(ctx)
            MyCommand.execute(config, flag)

    @staticmethod
    def execute(config: GlobalConfig, flag: str) -> None:
        if MyCommand.should_skip_output(config):
            return
        # Command implementation
```

### Type Safety

- All functions have type hints
- Pydantic models for configuration and data structures
- Protocol classes define interfaces
- Use `typing` and `typing-extensions` for advanced types
- Static analysis friendly with mypy

### Error Handling

- Commands should handle errors gracefully
- Use Rich console for error messages when not silent
- Preserve exit codes for scripting
- Debug mode provides detailed diagnostics

## Code Style Conventions

### Imports Organization

```python
# Standard library
import json
import time
from typing import Any, Dict, List

# Third-party
import click
from rich.console import Console
from rich.panel import Panel

# Local imports
from ..command_interface import BaseCommand, GlobalConfig
from ..utils import console, output_data, create_fancy_panel
```

### Function Signatures

```python
@staticmethod
def execute(config: GlobalConfig, option: str) -> None:
    """Execute the command with proper typing"""
    pass

@staticmethod
def _helper_method(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Private helper methods with descriptive names"""
    pass
```

### Data Structures

```python
# Use clear, descriptive data structures
output_data_structure = {
    "command_summary": {...},
    "items": [...],
    "statistics": {...}
}

# Add verbose details conditionally
if config.verbose:
    output_data_structure["verbose_details"] = {
        "config": config.model_dump(),
        "command_info": {...}
    }
```

## Utility Functions Reference

### Output Functions

- `output_data(data, config)`: Format data in JSON/YAML/Rich tables
- `create_data_table(title, columns, rows)`: Create styled Rich tables
- `console`: Global Rich console instance

### Animation Functions

- `create_rainbow_text(text)`: Generate rainbow-colored text
- `animate_spinner_with_text(text, duration)`: Animated spinners
- `create_fancy_panel(title, content, config)`: Bordered panels
- `show_welcome_animation(message, config)`: Standard welcome
- `show_completion_animation(message, config)`: Standard completion

### Helper Functions

- `print_debug_info(config, extra_info)`: Debug information display
- `get_output_format_from_config(config)`: Convert to OutputFormat enum
- `BaseCommand.get_config_from_context(ctx)`: Extract config from Click context
- `BaseCommand.should_skip_output(config)`: Check if silent mode

## Rich Library Usage

### Console Output

```python
# Import global console
from ..utils import console

# Colored text
rainbow_text = create_rainbow_text("My text")
console.print(rainbow_text)

# Tables
table = create_data_table("Title", columns, rows)
console.print(table)

# Panels
panel = create_fancy_panel("Title", "Content", config)
console.print(panel)
```

### Progress Bars

```python
from rich.progress import Progress

with Progress(console=console) as progress:
    task = progress.add_task("[green]Description...", total=count)
    for i in range(count):
        # Do work
        progress.update(task, advance=1)
```

## Package Management Commands

### Using uv

```bash
# Install dependencies
uv sync

# Add new dependencies
uv add package-name

# Run the CLI
uv run sandbox --help
uv run sandbox hello
uv run sandbox demo --count 5
uv run sandbox example --name "Claude" --style fancy
```

### Development Commands

```bash
# Run with different options
uv run sandbox --json hello
uv run sandbox --verbose demo
uv run sandbox --quiet --yaml demo --count 10

# Debug mode
uv run sandbox --debug hello
```

## Command Auto-Loading Details

### How It Works

1. `CommandRegistry` scans `sandbox.commands` package
2. Imports all `.py` files (except `__init__.py` and `_*` files)
3. Finds classes with `register_command` method
4. Calls `register_command(cli_group)` for each command
5. Commands become available in CLI automatically

### Registry Implementation

```python
# In command_interface.py
class CommandRegistry:
    def discover_commands(self) -> List[Type[CommandProtocol]]:
        # Uses importlib and pkgutil for discovery

    def register_all_commands(self, cli_group: click.Group) -> None:
        # Registers all discovered commands
```

### Main CLI Integration

```python
# In __init__.py main()
def main() -> None:
    registry = create_command_registry("sandbox.commands")
    registry.register_all_commands(cli)
    cli()
```

## Extension Guidelines

### New Commands

- Follow existing patterns for consistency
- Use `BaseCommand` inheritance
- Implement proper error handling
- Add comprehensive help text with emojis
- Test with all global flag combinations
- Use utility functions for common operations

### New Utilities

- Add to `utils.py` for shared functionality
- Respect global configuration flags
- Use Rich library components
- Include proper type hints and documentation

### Performance Considerations

- Early return for `config.silent` to skip processing
- Lazy loading of heavy operations
- Efficient Rich component usage
- Minimal overhead for quiet mode

## Testing Approach

When working on this project:

1. Test each command with all global flags (`--verbose`, `--json`, `--yaml`, `--debug`, `--quiet`, `--silent`)
2. Verify JSON/YAML output is valid and complete
3. Check animations work properly and respect quiet/silent
4. Ensure error cases are handled gracefully
5. Test auto-loading by adding/removing command files
6. Verify type hints with static analysis tools

## Dependencies Notes

- `rich>=14.0.0`: Core terminal UI library
- `click>=8.2.1`: CLI framework
- `pydantic>=2.0`: Data validation and configuration
- `pyyaml>=6.0.2`: YAML output support
- `typing-extensions`: Enhanced type hints for older Python versions

## Future Extension Ideas

### Command System Enhancements

- Plugin system with external command loading
- Command aliases and shortcuts
- Command categories and grouping
- Interactive command selection

### Feature Additions

- Configuration file support (YAML/TOML)
- Custom themes and color schemes
- Logging integration with Rich
- Command history and completion
- Template generation for new commands

### Advanced CLI Features

- Interactive mode with prompts
- Command pipelines and chaining
- Batch processing capabilities
- Real-time data monitoring commands
- Integration with external APIs

## Command Development Checklist

When creating a new command:

- [ ] Created new file in `commands/` directory
- [ ] Inherited from `BaseCommand`
- [ ] Implemented `register_command` static method
- [ ] Implemented `execute` static method
- [ ] Added proper type hints throughout
- [ ] Used utility functions appropriately
- [ ] Respected global configuration flags
- [ ] Added comprehensive help text
- [ ] Included error handling
- [ ] Tested with all global flags
- [ ] Verified auto-loading works
- [ ] Updated documentation if needed
