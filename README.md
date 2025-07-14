# Myriad Sandbox

A Python CLI tool demonstrating advanced terminal interfaces with animations, rainbow colors, and multiple output formats.

## Features

- 🌈 Rainbow text animations
- 📊 Rich terminal UI with tables and panels
- 📝 Multiple output formats (JSON, YAML, Rich)
- 🎛️ Global configuration flags
- 🔧 Modular command architecture with auto-loading
- 📦 Modern Python packaging with uv

## Installation

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd myriad

# Install dependencies
uv sync
```

## Usage

### Basic Commands

```bash
# Show help
uv run sandbox --help

# Run hello command
uv run sandbox hello

# Run demo with options
uv run sandbox demo --count 5 --speed 0.1

# Run example command
uv run sandbox example --name "World" --style fancy --repeat 3
```

### Output Formats

```bash
# JSON output
uv run sandbox --json hello

# YAML output
uv run sandbox --yaml demo

# Default rich output (tables and panels)
uv run sandbox hello
```

### Global Flags

```bash
# Verbose mode (extra details)
uv run sandbox --verbose demo

# Debug mode (development info)
uv run sandbox --debug hello

# Quiet mode (minimal output)
uv run sandbox --quiet demo

# Silent mode (no output)
uv run sandbox --silent hello
```

## Architecture

This project showcases modern Python CLI development with:

- **Click**: Command-line interface framework
- **Rich**: Terminal styling and animations
- **Pydantic**: Data validation and configuration
- **Modular Commands**: Auto-loading command system
- **Type Safety**: Full type hints throughout

## Development

### Adding New Commands

1. Create a new file in `src/sandbox/commands/`
2. Inherit from `BaseCommand`
3. Implement `register_command` and `execute` methods
4. The command will be auto-loaded on next run

### Package Management

```bash
# Add dependencies
uv add package-name

# Update dependencies
uv sync

# Run tests
uv run python -m pytest

# Type checking
uv run mypy src/
```

## Available Commands

- **hello**: Basic greeting with rainbow animations
- **demo**: Advanced demo with progress bars and statistics
- **example**: Template command showing all features

Run `uv run sandbox --help` for complete command documentation.
