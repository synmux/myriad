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

| Flag | Short | Description |
|------|-------|-------------|
| `--verbose` | `-v` | Enable verbose output with additional details |
| `--json` | `-j` | Output data in JSON format |
| `--yaml` | `-y` | Output data in YAML format |
| `--debug` | `-d` | Enable debug mode with diagnostic info |
| `--quiet` | `-q` | Suppress animations and progress indicators |
| `--silent` | `-s` | Suppress all output completely |

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

```
src/sandbox/
├── __init__.py              # Main CLI entry point with auto-loading
├── command_interface.py     # Base command interface and registry
├── utils.py                 # Shared utilities for all commands
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

### Adding New Commands

Creating a new command is straightforward:

1. **Create a new file** in `src/sandbox/commands/`
2. **Implement the command class** inheriting from `BaseCommand`
3. **Define the `register_command` static method**
4. **The command will be auto-loaded** on the next run

#### Command Template

```python
"""
My new command for Sandbox CLI
"""

import click
from ..command_interface import BaseCommand, GlobalConfig
from ..utils import console, output_data, print_debug_info

class MyCommand(BaseCommand):
    """My new command description"""

    @staticmethod
    def register_command(cli_group: click.Group) -> None:
        """Register the command with the CLI group"""

        @cli_group.command()
        @click.option('--my-option', help='My custom option')
        @click.pass_context
        def mycommand(ctx: click.Context, my_option: str) -> None:
            """
            🎯 My new command description!
            
            Detailed description of what this command does.
            """
            config = MyCommand.get_config_from_context(ctx)
            MyCommand.execute(config, my_option)

    @staticmethod
    def execute(config: GlobalConfig, my_option: str) -> None:
        """Execute the command"""
        if MyCommand.should_skip_output(config):
            return

        print_debug_info(config, {"command": "mycommand"})
        
        # Your command logic here
        data = {"message": f"Hello from my command! Option: {my_option}"}
        output_data(data, config)
```

#### Best Practices

1. **Inherit from BaseCommand** for consistent interface
2. **Use the utility functions** for output, animations, and formatting
3. **Respect global flags** (quiet, silent, verbose, debug)
4. **Include comprehensive help text** with emojis for visual appeal
5. **Add proper type hints** throughout your code
6. **Handle errors gracefully** and preserve exit codes
7. **Test with all global flag combinations**

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

The `utils.py` module provides common functionality:

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

---

**Built with ❤️ using Python, Click, Rich, and lots of rainbow colors! 🌈**