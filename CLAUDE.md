# CLAUDE.md - AI Assistant Project Context

## Project Overview

This is a Python-based CLI tool called "Sandbox" that demonstrates advanced terminal user interfaces with animations, rainbow colors, and multiple output formats. The project showcases modern Python CLI development patterns using `click`, `rich`, and `pydantic`.

## Project Structure

```
myriad/
├── src/sandbox/
│   └── __init__.py          # Main CLI module with all commands
├── pyproject.toml           # Python project configuration
├── uv.lock                  # Dependency lock file
├── README.md                # User documentation
└── CLAUDE.md                # This file - AI assistant context
```

## Key Technologies

- **Package Management**: `uv` (fast Python package manager)
- **CLI Framework**: `click` (command-line interface creation)
- **Terminal UI**: `rich` (rich text and beautiful formatting)
- **Data Validation**: `pydantic` (data validation and settings)
- **Type System**: Full type hints with `typing` and `typing-extensions`
- **Output Formats**: JSON, YAML, Rich tables/panels

## Architecture Patterns

### Global Configuration
- Uses `GlobalConfig` Pydantic model for consistent settings across all commands
- Configuration passed through Click context object
- Supports: verbose, debug, quiet, silent modes + output formats

### Command Structure
- Main CLI group with global flags: `--verbose`, `--json`, `--yaml`, `--debug`, `--quiet`, `--silent`
- Subcommands inherit global configuration automatically
- Each command accesses config via `ctx.obj['config']`

### Output Handling
- Centralized `output_data()` function handles all three formats
- Respects quiet/silent flags for animations and output
- Rich library used for colorful terminal output in normal mode

### Animation System
- `create_rainbow_text()`: Multi-color text rendering
- `animate_spinner_with_text()`: Progress spinners with custom messages
- `create_fancy_panel()`: Bordered panels with styling
- All animations respect quiet/silent flags

## Current Commands

### `hello`
- Basic "hello world" with rainbow animations
- Demonstrates: panels, spinners, data output, all flags
- Shows sample data structure with timestamps and metadata

### `demo`
- Advanced demo with progress bars and ASCII art
- Options: `--count` (items to process), `--speed` (animation speed)  
- Demonstrates: multi-task progress, tables, complex data structures
- Shows statistical calculations and summaries

## Development Patterns

### Adding New Commands
1. Create function decorated with `@cli.command()`
2. Add `@click.pass_context` to access global config
3. Use `config: GlobalConfig = ctx.obj['config']` pattern
4. Early return if `config.silent` for performance
5. Use `output_data()` for consistent output formatting
6. Respect `config.quiet` for animations

### Type Safety
- All functions have type hints
- Pydantic models for configuration and data structures
- Use `typing` and `typing-extensions` for advanced types

### Error Handling
- Commands should handle errors gracefully
- Use Rich console for error messages when not silent
- Preserve exit codes for scripting

## Code Style Conventions

### Imports
```python
import json
import time
from enum import Enum
from typing import Any, Dict, Optional

import click
import yaml
from rich.console import Console
from rich.panel import Panel
# ... other rich imports
from pydantic import BaseModel
```

### Function Signatures
```python
def my_function(param: str, config: GlobalConfig) -> None:
    """Function with type hints and docstring"""
    pass

@cli.command()
@click.option('--flag', help='Description')
@click.pass_context
def my_command(ctx: click.Context, flag: str) -> None:
    """Command docstring shown in help"""
    config: GlobalConfig = ctx.obj['config']
```

### Data Structures
```python
# Use clear, descriptive data structures
output_data_structure = {
    "summary": {...},
    "items": [...],
    "statistics": {...}
}

# Add verbose details conditionally
if config.verbose:
    output_data_structure["verbose_details"] = {...}
```

## Rich Library Usage

### Console Output
```python
# Global console instance
console = Console()

# Colored text
rainbow_text = create_rainbow_text("My text")
console.print(rainbow_text)

# Tables
table = Table(title="My Table", box=box.ROUNDED)
table.add_column("Column", style="cyan")
table.add_row("Value")
console.print(table)

# Panels
panel = create_fancy_panel("Title", "Content", config)
console.print(panel)
```

### Progress Bars
```python
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

## Extension Guidelines

### New Subcommands
- Follow existing patterns for consistency
- Add appropriate click options for command-specific flags
- Use descriptive help text with emojis for visual appeal
- Implement proper data structures for output
- Test with all global flag combinations

### New Output Formats
- Extend `OutputFormat` enum
- Update `output_data()` function
- Add corresponding global flag
- Maintain backwards compatibility

### New Animation Types
- Create reusable functions in the main module
- Respect quiet/silent flags
- Use Rich library components
- Keep performance reasonable

## Testing Approach

When working on this project:
1. Test each command with all global flags
2. Verify JSON/YAML output is valid and complete
3. Check animations work properly and respect quiet/silent
4. Ensure error cases are handled gracefully
5. Test with various count/speed combinations for demo

## Dependencies Notes

- `rich>=14.0.0`: Core terminal UI library
- `click>=8.2.1`: CLI framework
- `pydantic>=2.0`: Data validation (version should be compatible)
- `pyyaml>=6.0.2`: YAML output support
- `typing-extensions`: Enhanced type hints

## Future Extension Ideas

- File I/O commands with progress tracking
- Network operations with real-time updates
- Data processing pipelines with multi-step progress
- Configuration file support
- Plugin system for custom commands
- Interactive mode with prompts
- Logging integration with Rich
- Custom themes and color schemes