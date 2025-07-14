# 🌈 Sandbox CLI - A Delightfully Animated Command-Line Tool

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/daveio/myriad)

A fun and colorful CLI tool built with Python that demonstrates animated output, rainbow colors, progress bars, and multiple output formats. Features a modular command architecture with auto-loading for easy extensibility.

## ✨ Features

### 🎨 Visual Excellence

- **Rainbow-colored output** with animated text
- **Animated ASCII art** and fancy bordered panels
- **Progress bars and spinners** for visual feedback
- **Rich table formatting** with customizable styling

### 🔧 Technical Architecture

- **Modular command system** with auto-loading from `commands/` directory
- **Typed Python** with full type hints and Pydantic models
- **Multiple output formats**: Rich tables, JSON, YAML
- **Global flags** that work consistently across all subcommands
- **Extensible design** for easy addition of new commands

### 🎛️ Configuration Options

- **Verbosity levels**: verbose, quiet, silent, debug modes
- **Output format control**: normal, JSON, YAML
- **Animation control**: respectful of quiet/silent flags
- **Debug mode**: comprehensive diagnostic information

## 🚀 Installation

This project uses `uv` for package management and `mise` for Python version management.

```bash
# Clone the repository
git clone <repository-url>
cd myriad

# Install dependencies
uv sync

# The CLI tool is available as 'sandbox'
uv run sandbox --help
```

### Requirements

- Python 3.13+
- `uv` package manager
- Terminal with color support (most modern terminals)

## 📖 Usage

### Global Flags

All subcommands support these global flags:

| Flag        | Short | Description                                   |
| ----------- | ----- | --------------------------------------------- |
| `--verbose` | `-v`  | Enable verbose output with additional details |
| `--json`    | `-j`  | Output data in JSON format                    |
| `--yaml`    | `-y`  | Output data in YAML format                    |
| `--debug`   | `-d`  | Enable debug mode with diagnostic info        |
| `--quiet`   | `-q`  | Suppress animations and progress indicators   |
| `--silent`  | `-s`  | Suppress all output completely                |

### Basic Commands

```bash
# Get help
uv run sandbox --help

# List all available commands
uv run sandbox --help

# Get help for a specific command
uv run sandbox hello --help
```

## 🎯 Available Commands

### `hello` - Spectacular Hello World

A delightful hello world command demonstrating all visual capabilities.

```bash
# Basic usage
uv run sandbox hello

# With different output formats
uv run sandbox --json hello
uv run sandbox --yaml hello

# Verbose mode with extra details
uv run sandbox --verbose hello

# Quiet mode (no animations)
uv run sandbox --quiet hello
```

**Features demonstrated:**

- Rainbow text rendering
- Fancy panels with borders
- Spinner animations
- Multiple output formats
- Global flag integration

### `demo` - Advanced Feature Showcase

An advanced demonstration with progress bars, ASCII art, and complex data structures.

```bash
# Basic demo
uv run sandbox demo

# Customize processing
uv run sandbox demo --count 10 --speed 0.2

# Different output formats
uv run sandbox --json demo --count 3
uv run sandbox --yaml demo --count 5
```

**Options:**

- `--count`, `-c`: Number of demo items to process (default: 5)
- `--speed`, `-s`: Animation speed in seconds per step (default: 0.1)

**Features demonstrated:**

- ASCII art banner animation
- Multi-task progress tracking
- Dynamic data generation
- Rich table formatting
- Statistical calculations

### `example` - Command Creation Pattern

A template command showing how to create new commands that integrate with the system.

```bash
# Basic example
uv run sandbox example

# Customized greeting
uv run sandbox example --name "Claude" --repeat 3 --style animated

# Different styles
uv run sandbox example --style simple
uv run sandbox example --style fancy
uv run sandbox example --style animated
```

**Options:**

- `--name`, `-n`: Name to greet (default: "World")
- `--repeat`, `-r`: Number of times to repeat the greeting (default: 1)
- `--style`, `-st`: Style of greeting (`simple`, `fancy`, `animated`)

**Features demonstrated:**

- Command-specific options
- Multiple output styles
- Conditional animations
- Error handling patterns

## 🛠️ Development

### Project Structure

```plaintext
src/sandbox/
├── __init__.py              # Main CLI entry point with auto-loading
├── command_interface.py     # Base command interface and registry
├── util/                    # Shared utilities package
│   └── __init__.py         # Utilities for all commands
└── commands/                # Auto-loaded command modules
    ├── __init__.py         # Commands package
    ├── hello.py           # Hello world command
    ├── demo.py            # Advanced demo command
    └── example.py         # Example command template
```

### Command Architecture

The CLI uses a modular architecture where commands are automatically discovered and loaded from the `commands/` directory.

#### Key Components

1. **BaseCommand**: Abstract base class all commands inherit from
2. **CommandProtocol**: Type protocol defining the command interface
3. **CommandRegistry**: Auto-discovery and registration system
4. **GlobalConfig**: Pydantic model for global configuration
5. **Shared Utilities**: Common functions for output, animations, etc.

### Auto-Loading Feature

The CLI uses an innovative **auto-loading system** that automatically discovers and registers commands without manual configuration:

#### How Auto-Loading Works

1. **Automatic Discovery**: When the CLI starts, it scans the `src/sandbox/commands/` directory
2. **Module Loading**: All `.py` files (except `__init__.py` and files starting with `_`) are imported
3. **Class Detection**: The system finds classes that implement the `CommandProtocol` interface
4. **Registration**: Each command's `register_command()` method is called automatically
5. **Availability**: Commands become immediately available in the CLI

#### Benefits

- ✅ **Zero Configuration**: No manual registration required
- ✅ **Instant Integration**: Drop a file in `commands/` and it works
- ✅ **Type Safety**: Protocol ensures all commands follow the same interface
- ✅ **Error Isolation**: Failed command loading doesn't break other commands
- ✅ **Development Speed**: Focus on command logic, not infrastructure

#### What Gets Auto-Loaded

```python
# ✅ These files will be auto-loaded:
commands/hello.py       # Contains HelloCommand class
commands/demo.py        # Contains DemoCommand class
commands/mycommand.py   # Contains MyCommand class

# ❌ These files will be ignored:
commands/__init__.py    # Package initialization file
commands/_private.py    # Files starting with underscore
commands/util.py        # Files without CommandProtocol classes
```

#### Auto-Loading Requirements

For a command to be auto-loaded, it must:

1. **Be in the right location**: `src/sandbox/commands/filename.py`
2. **Implement the interface**: Have a class that implements `CommandProtocol`
3. **Have the method**: Include a static `register_command()` method
4. **Be valid Python**: No syntax errors that prevent import

#### Troubleshooting Auto-Loading

If your command isn't appearing:

```bash
# Check for import errors
uv run python -c "from sandbox.commands import mycommand"

# Enable debug mode to see loading issues
uv run sandbox --debug --help

# Verify file structure
ls -la src/sandbox/commands/
```

The auto-loading system will show warnings for any commands that fail to load, helping you diagnose issues quickly.

### Adding New Commands

Creating a new command is straightforward thanks to the auto-loading architecture. Here's a complete step-by-step guide:

#### Step-by-Step Instructions

1. **Create a new file** in `src/sandbox/commands/` (e.g., `mycommand.py`)
2. **Import required modules** and inherit from `BaseCommand`
3. **Implement the command class** with required methods
4. **Test your command** with all global flags
5. **The command will be auto-loaded** on the next run - no manual registration needed!

#### Complete Working Example

Let's create a new command called `greet` that demonstrates all the patterns:

**Step 1**: Create `src/sandbox/commands/greet.py`:

```python
"""
Greet command for Sandbox CLI

A friendly greeting command that demonstrates command creation patterns.
"""

import time
from typing import Any, override

import click

from ..command_interface import BaseCommand, GlobalConfig
from ..utils import (
    console,
    create_fancy_panel,
    output_data,
    show_welcome_animation,
    show_completion_animation,
    print_debug_info,
    create_rainbow_text,
)


class GreetCommand(BaseCommand):
    """A friendly greeting command with customizable options"""

    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        """Register the greet command with the CLI group"""

        @cli_group.command()
        @click.option('--name', '-n', default='Friend', help='Name of person to greet')
        @click.option('--style', '-s',
                      type=click.Choice(['casual', 'formal', 'enthusiastic']),
                      default='casual', help='Greeting style to use')
        @click.option('--language', '-l',
                      type=click.Choice(['en', 'es', 'fr']),
                      default='en', help='Language for greeting')
        @click.pass_context
        def greet(ctx: click.Context, name: str, style: str, language: str) -> None:
            """
            👋 Greet someone with style and flair!

            This command demonstrates how to create new commands with:
            - Custom command-line options
            - Multiple choice parameters
            - Animated output and panels
            - Proper global flag integration

            Examples:
              sandbox greet --name Alice --style enthusiastic
              sandbox greet -n Bob -s formal -l es
            """
            config = GreetCommand.get_config_from_context(ctx)
            GreetCommand.execute(config, name, style, language)

    @staticmethod
    def execute(config: GlobalConfig, name: str, style: str, language: str) -> None:
        """Execute the greet command with the given parameters"""
        if GreetCommand.should_skip_output(config):
            return

        # Debug info if enabled
        print_debug_info(config, {
            "command": "greet",
            "parameters": {"name": name, "style": style, "language": language}
        })

        # Welcome animation
        show_welcome_animation("greeting generator", config)

        # Generate greeting based on parameters
        greeting_data = GreetCommand._generate_greeting(name, style, language)

        # Show fancy greeting panel
        if not config.quiet:
            greeting_panel = create_fancy_panel(
                f"🎉 {greeting_data['greeting_type']} 🎉",
                greeting_data['message'],
                config
            )
            console.print(greeting_panel)

        # Create comprehensive output data
        output_structure = GreetCommand._create_output_data(
            name, style, language, greeting_data, config
        )

        # Output data in requested format
        output_data(output_structure, config)

        # Completion animation
        show_completion_animation("greeting", config)

    @staticmethod
    def _generate_greeting(name: str, style: str, language: str) -> dict[str, Any]:
        """Generate greeting message based on parameters"""
        greetings = {
            'en': {
                'casual': f"Hey there, {name}! How's it going?",
                'formal': f"Good day, {name}. I hope you are well.",
                'enthusiastic': f"WOW! Hello {name}! Amazing to see you! 🎉"
            },
            'es': {
                'casual': f"¡Hola {name}! ¿Qué tal?",
                'formal': f"Buenos días, {name}. Espero que esté bien.",
                'enthusiastic': f"¡¡¡HOLA {name}!!! ¡Qué emocionante verte! 🎉"
            },
            'fr': {
                'casual': f"Salut {name}! Comment ça va?",
                'formal': f"Bonjour {name}. J'espère que vous allez bien.",
                'enthusiastic': f"BONJOUR {name}! Fantastique de vous voir! 🎉"
            }
        }

        greeting_types = {
            'casual': 'Casual Greeting',
            'formal': 'Formal Greeting',
            'enthusiastic': 'Enthusiastic Greeting'
        }

        return {
            'message': greetings[language][style],
            'greeting_type': greeting_types[style],
            'language': language,
            'style': style,
            'target_name': name,
            'timestamp': time.time()
        }

    @staticmethod
    def _create_output_data(
        name: str,
        style: str,
        language: str,
        greeting_data: dict[str, Any],
        config: GlobalConfig
    ) -> dict[str, Any]:
        """Create comprehensive output data structure"""
        output_data_structure: dict[str, Any] = {
            "command_info": {
                "name": "greet",
                "parameters": {
                    "name": name,
                    "style": style,
                    "language": language
                },
                "execution_time": time.time()
            },
            "greeting": greeting_data,
            "metadata": {
                "available_styles": ["casual", "formal", "enthusiastic"],
                "available_languages": ["en", "es", "fr"],
                "message_length": len(greeting_data['message'])
            }
        }

        if config.verbose:
            verbose_info: dict[str, Any] = {
                "config": config.model_dump(),
                "command_features": [
                    "Multi-language support",
                    "Multiple greeting styles",
                    "Animated output",
                    "Global flag integration"
                ],
                "development_notes": {
                    "architecture": "Modular command with auto-loading",
                    "patterns_used": ["BaseCommand inheritance", "Type hints", "Rich UI"]
                }
            }
            output_data_structure["verbose_details"] = verbose_info

        return output_data_structure
```

**Step 2**: Test your new command:

```bash
# Test basic functionality
uv run sandbox greet --name Alice

# Test with options
uv run sandbox greet --name Bob --style formal --language es

# Test with global flags
uv run sandbox --json greet --name Charlie --style enthusiastic
uv run sandbox --verbose greet --name Diana --language fr
uv run sandbox --quiet greet --name Eve
```

**Step 3**: Verify auto-loading worked:

```bash
# Check that your command appears in help
uv run sandbox --help

# Get help for your specific command
uv run sandbox greet --help
```

#### Command Development Best Practices

1. **Follow the Pattern**: Always inherit from `BaseCommand` and use `@override`
2. **Type Everything**: Use proper type hints for all parameters and return values
3. **Respect Global Flags**: Check `config.silent`, `config.quiet`, etc.
4. **Use Utility Functions**: Leverage shared utilities for consistency
5. **Rich Help Text**: Include emojis and examples in docstrings
6. **Error Handling**: Use try/catch and preserve exit codes
7. **Test Thoroughly**: Test with all global flag combinations

#### Common Patterns

**Simple Command Structure**:

```python
@staticmethod
@override
def register_command(cli_group: click.Group) -> None:
    @cli_group.command()
    @click.option('--option', help='Description')
    @click.pass_context
    def mycommand(ctx: click.Context, option: str) -> None:
        config = MyCommand.get_config_from_context(ctx)
        MyCommand.execute(config, option)

@staticmethod
def execute(config: GlobalConfig, option: str) -> None:
    if MyCommand.should_skip_output(config):
        return
    # Command logic here
```

**Data Output Pattern**:

```python
# Create structured data
data = {
    "command_info": {...},
    "results": [...],
    "metadata": {...}
}

# Add verbose details if requested
if config.verbose:
    data["verbose_details"] = {...}

# Output in requested format (JSON/YAML/Rich)
output_data(data, config)
```

#### Troubleshooting

**Command not appearing?**

- Check file is in `src/sandbox/commands/`
- Ensure class inherits from `BaseCommand`
- Verify `register_command` method exists
- Check for Python syntax errors

**Type checking issues?**

```bash
# Run type checkers
uv run mypy src/sandbox/ --strict
uv run basedpyright src/sandbox/
```

**Testing checklist:**

- [ ] `uv run sandbox mycommand` (basic)
- [ ] `uv run sandbox --json mycommand` (JSON output)
- [ ] `uv run sandbox --yaml mycommand` (YAML output)
- [ ] `uv run sandbox --verbose mycommand` (verbose)
- [ ] `uv run sandbox --quiet mycommand` (quiet)
- [ ] `uv run sandbox --silent mycommand` (silent)
- [ ] `uv run sandbox --debug mycommand` (debug)
- [ ] `uv run sandbox mycommand --help` (help)

#### Quick Reference

For experienced developers, here's the essential template:

```python
from typing import Any, override
import click
from ..command_interface import BaseCommand, GlobalConfig
from ..utils import output_data, print_debug_info

class MyCommand(BaseCommand):
    @staticmethod
    @override
    def register_command(cli_group: click.Group) -> None:
        @cli_group.command()
        @click.option('--option', help='Description')
        @click.pass_context
        def mycommand(ctx: click.Context, option: str) -> None:
            """🎯 Command description!"""
            config = MyCommand.get_config_from_context(ctx)
            MyCommand.execute(config, option)

    @staticmethod
    def execute(config: GlobalConfig, option: str) -> None:
        if MyCommand.should_skip_output(config):
            return
        print_debug_info(config, {"command": "mycommand"})
        data = {"result": f"Processed {option}"}
        output_data(data, config)
```

**Essential Commands:**

```bash
# Test your command
uv run sandbox mycommand --option value

# Test with all flags
uv run sandbox --json --verbose mycommand

# Check types
uv run mypy src/sandbox/ --strict
```

### Development Commands

```bash
# Install dependencies
uv sync

# Add new dependencies
uv add package-name

# Run with different configurations
uv run sandbox --json hello
uv run sandbox --verbose demo
uv run sandbox --quiet --yaml demo --count 10

# Debug mode for development
uv run sandbox --debug hello
```

### Utility Functions

The `util` package provides common functionality:

#### Output Functions

- `output_data()`: Format data in JSON, YAML, or Rich tables
- `create_data_table()`: Create styled Rich tables
- `console`: Global Rich console instance

#### Animation Functions

- `create_rainbow_text()`: Generate rainbow-colored text
- `animate_spinner_with_text()`: Animated spinners
- `create_fancy_panel()`: Bordered panels with styling
- `show_welcome_animation()`: Standard welcome animation
- `show_completion_animation()`: Standard completion animation

#### Helper Functions

- `print_debug_info()`: Debug information display
- `get_output_format_from_config()`: Convert config to OutputFormat enum

## 🔍 Technical Details

### Dependencies

- **click**: Command-line interface framework
- **rich**: Rich text and beautiful formatting
- **pydantic**: Data validation and settings management
- **pyyaml**: YAML output support
- **typing-extensions**: Enhanced type hints

### Type Safety

The project uses comprehensive type hints:

- Pydantic models for configuration
- Protocol classes for interfaces
- Type hints on all functions and methods
- Generic types where appropriate

### Error Handling

- Commands handle errors gracefully
- Rich console used for error messages (when not silent)
- Exit codes preserved for scripting
- Debug mode provides detailed error information

### Performance Considerations

- Early returns for silent mode to skip unnecessary processing
- Lazy loading of command modules
- Efficient Rich components usage
- Minimal overhead for quiet mode operations

## 🎯 Usage Examples

### Basic Usage

```bash
# Normal colorful output
uv run sandbox hello

# JSON output for scripting
uv run sandbox --json demo --count 5 | jq '.statistics'

# YAML output for configuration
uv run sandbox --yaml hello > output.yaml
```

### Development and Debugging

```bash
# Verbose mode for detailed information
uv run sandbox --verbose demo --count 3

# Debug mode for troubleshooting
uv run sandbox --debug hello

# Quiet mode for automated scripts
uv run sandbox --quiet demo --count 100
```

### Integration Examples

```bash
# Silent mode for scripts (exit code only)
if uv run sandbox --silent hello; then
    echo "Command succeeded"
fi

# JSON output for data processing
uv run sandbox --json demo --count 10 | python process_data.py

# Combine with other tools
uv run sandbox --yaml demo | yq '.statistics.avg_score'
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** for your new command or enhancement
3. **Follow the existing patterns** and code style
4. **Add comprehensive documentation** for new features
5. **Test with all global flags** and edge cases
6. **Submit a pull request** with a clear description

### Code Style

- Use type hints throughout
- Follow the existing command structure
- Include docstrings for all functions and classes
- Use descriptive variable and function names
- Respect the global configuration in all commands

## 📄 License

See LICENSE file for details.
