# 🌈 Sandbox CLI - A Delightfully Animated Command-Line Tool

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/daveio/myriad)

A fun and colorful CLI tool built with Python that demonstrates animated output, rainbow colors, progress bars, and multiple output formats. Perfect for learning CLI development patterns and showcasing rich terminal interfaces.

## ✨ Features

- 🎨 **Rainbow-colored output** with animated text
- 📊 **Multiple output formats**: Normal (rich tables), JSON, YAML
- 🎯 **Global flags** that work across all subcommands
- 📈 **Progress bars and spinners** for visual feedback
- 🎭 **ASCII art animations** and fancy panels
- 🔧 **Extensible subcommand structure** for easy expansion
- 🎛️ **Configurable verbosity levels** (verbose, quiet, silent, debug)

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

## 📖 Usage

### Basic Commands

```bash
# Get help
uv run sandbox --help

# Hello world with animations
uv run sandbox hello

# Advanced demo with progress bars
uv run sandbox demo

# Demo with custom options
uv run sandbox demo --count 10 --speed 0.1
```

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

### Examples

```bash
# Normal colorful output
uv run sandbox hello

# JSON output format
uv run sandbox --json hello

# YAML output format  
uv run sandbox --yaml hello

# Verbose mode with extra details
uv run sandbox --verbose hello

# Quiet mode (no animations)
uv run sandbox --quiet demo --count 5

# Silent mode (no output at all)
uv run sandbox --silent hello

# Debug mode with configuration details
uv run sandbox --debug demo
```

## 🔧 Available Subcommands

### `hello`
A spectacular hello world command that demonstrates:
- Rainbow-colored text animations
- Fancy bordered panels
- Spinner animations with custom messages
- Sample data output in multiple formats

```bash
uv run sandbox hello
uv run sandbox --verbose hello
uv run sandbox --json hello
```

### `demo`
An advanced demonstration showcasing:
- Animated ASCII art banners
- Multi-task progress bars
- Dynamic data generation
- Rich table formatting
- Statistical summaries

```bash
uv run sandbox demo
uv run sandbox demo --count 10 --speed 0.2
uv run sandbox --yaml demo --count 3
```

#### Demo Options
- `--count`, `-c`: Number of demo items to process (default: 5)
- `--speed`, `-s`: Animation speed in seconds per step (default: 0.1)

## 🛠️ Development

### Project Structure

```
src/sandbox/
├── __init__.py          # Main CLI module with all commands
└── ...                  # Additional modules (future expansion)
```

### Adding New Subcommands

The CLI uses the `click` library for command structure. To add a new subcommand:

1. Define a new function decorated with `@cli.command()`
2. Use `@click.pass_context` to access global configuration
3. Access the global config with `config: GlobalConfig = ctx.obj['config']`
4. Implement output format handling with `output_data()`
5. Respect the quiet/silent flags for animations

Example template:

```python
@cli.command()
@click.option('--custom-flag', help='Custom option for this command')
@click.pass_context
def my_command(ctx: click.Context, custom_flag: str) -> None:
    """My awesome new command"""
    config: GlobalConfig = ctx.obj['config']
    
    if config.silent:
        return
    
    # Your command logic here
    data = {"message": "Hello from my command!"}
    output_data(data, config)
```

### Dependencies

- **click**: Command-line interface framework
- **rich**: Rich text and beautiful formatting
- **pydantic**: Data validation and settings management
- **pyyaml**: YAML output support
- **typing-extensions**: Enhanced type hints

### Code Quality

The project uses:
- Type hints throughout
- Pydantic models for configuration
- Rich console for all output
- Consistent error handling
- Modular design patterns

## 🎨 Technical Details

### Global Configuration

The `GlobalConfig` class manages all global CLI settings:

```python
class GlobalConfig(BaseModel):
    verbose: bool = False
    debug: bool = False  
    quiet: bool = False
    silent: bool = False
    output_format: OutputFormat = OutputFormat.NORMAL
```

### Output Formats

Three output formats are supported:
- **Normal**: Rich tables, panels, and colorful text
- **JSON**: Machine-readable JSON with proper formatting  
- **YAML**: Human-readable YAML format

### Animation System

The tool includes several animation utilities:
- `create_rainbow_text()`: Generate rainbow-colored text
- `animate_spinner_with_text()`: Animated spinners with custom messages
- `create_fancy_panel()`: Bordered panels with rainbow styling

## 📋 Requirements

- Python 3.13+
- `uv` package manager
- Terminal with color support (most modern terminals)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your subcommand or enhancement
4. Follow the existing code patterns
5. Test with all global flags
6. Submit a pull request

## 📄 License

See LICENSE file for details.
