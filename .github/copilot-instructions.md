# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Note**: `CLAUDE.md` and `AGENTS.md` are symlinks to `.github/copilot-instructions.md` - update only `.github/copilot-instructions.md` to update all AI instruction files.

## Project Overview

Myriad is a Python-based CLI tool called "Sandbox" that serves as a personal AI sandbox for experimenting with AI integrations (OpenAI, Anthropic) while demonstrating advanced terminal user interfaces with animations, rainbow colors, and multiple output formats. The project showcases modern Python CLI development patterns using `click`, `rich`, and `pydantic` with a **modular command architecture** that auto-loads commands from a dedicated directory structure.

## Development Commands

```bash
# Install dependencies and set up environment
uv sync

# Run the CLI (using uv)
uv run sandbox --help

# Run specific commands
uv run sandbox struct --word "amazing" --context "The view was amazing"
uv run sandbox demo --count 10 --speed fast
uv run sandbox example --name "Claude" --style animated

# Run with different output formats
uv run sandbox --json struct --word "test"
uv run sandbox --yaml demo
uv run sandbox --debug example --name "Debug Mode"

# Launch Claude Code assistant
mise run claude
# Or use the bin script
./bin/claude
```

## Project Structure

```plaintext
myriad/
├── src/sandbox/
│   ├── __init__.py              # Main CLI entry point with auto-loading
│   ├── command_interface.py     # Base command interface and registry system
│   ├── util/                    # Shared utilities package
│   │   ├── __init__.py         # Core utilities for all commands
│   │   └── ai.py               # AI integration (OpenAI/OpenRouter via Cloudflare AI Gateway)
│   └── commands/                # Auto-loaded command modules
│       ├── __init__.py         # Commands package
│       ├── struct.py           # AI-powered word suggestion command
│       ├── demo.py             # Advanced demo command
│       └── example.py          # Example command template
├── bin/                         # Convenience scripts
│   ├── claude                  # Launch Claude Code
│   └── sandbox                 # Run sandbox CLI
├── mise.toml                   # Development environment configuration
├── pyproject.toml              # Python project configuration
├── uv.lock                     # Dependency lock file
├── README.md                   # User documentation
└── CLAUDE.md                   # This file - AI assistant context
```

## Key Technologies

- **Environment Management**: `mise` (development environment and task runner)
- **Package Management**: `uv` (fast Python package manager)
- **Python Version**: 3.13.5
- **CLI Framework**: `click` (command-line interface creation)
- **Terminal UI**: `rich` (rich text and beautiful formatting)
- **Data Validation**: `pydantic` (data validation and settings)
- **AI Integration**:
  - `openai` SDK for OpenRouter access
  - `anthropic` SDK for Claude integration
  - `instructor` for structured AI outputs
  - Cloudflare AI Gateway for caching, rate limiting, and monitoring
- **Type System**: Full type hints with `typing` and `typing-extensions`
- **Output Formats**: JSON, YAML, Rich tables/panels

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

### AI Integration Architecture

- Centralized AI client configuration in `util/ai.py`
- Supports Cloudflare AI Gateway integration with:
  - Request caching (with TTL and custom cache keys)
  - Automatic retries with configurable backoff strategies
  - Request timeouts and rate limiting
  - Cost tracking and event monitoring
- Environment variables required:
  - `OPENROUTER_API_KEY` for OpenRouter access
  - `CLOUDFLARE_AI_GATEWAY_TOKEN` for AI Gateway authentication
  - Optional: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` for direct access

## Current Commands

### `struct` (`commands/struct.py`)

- AI-powered word suggestion command using OpenRouter
- Demonstrates structured JSON output from LLMs
- Options: `--word` (required), `--context` (optional for better suggestions)
- Uses JSON schema validation for consistent AI responses

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
   from ..util import console, output_data, print_debug_info
   ```
3. **Create command class** inheriting from `BaseCommand`
4. **Implement `register_command` static method**
5. **Define `execute` static method** with command logic
6. **Use utility functions** for consistent behavior
7. **Command automatically loads** on next CLI run

### AI Integration Pattern

```python
from ..util.ai import get_openai_client, AIGatewayConfig, BackoffType

# Simple usage with caching disabled
client = get_openai_client(enable_caching=False)

# Advanced usage with full gateway configuration
gateway_config = AIGatewayConfig(
    enable_caching=True,
    cache_ttl=3600,  # 1 hour
    max_attempts=3,
    retry_delay=1000,  # 1 second
    backoff_type=BackoffType.EXPONENTIAL,
    metadata={"command": "struct", "version": "1.0"}
)
client = get_openai_client(gateway_config=gateway_config)

# Make structured API calls
response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[...],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "response_name",
            "strict": True,
            "schema": {...}
        }
    }
)
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

### AI Functions

- `get_openai_client(enable_caching, gateway_config)`: OpenAI client via Cloudflare Gateway
- `get_api_key(service)`: Retrieve API keys from environment
- `AIGatewayConfig`: Configure caching, retries, timeouts, and monitoring
- `BackoffType`: Enum for retry strategies (CONSTANT, LINEAR, EXPONENTIAL)

## Environment Configuration

### Required Environment Variables

```bash
# For AI features
OPENROUTER_API_KEY=your_openrouter_key
CLOUDFLARE_AI_GATEWAY_TOKEN=your_cloudflare_token

# Optional for direct access
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Cloudflare AI Gateway Settings

The project is configured to use:

- Account ID: `def50674a738cee409235f71819973cf`
- Gateway ID: `ai-dave-io`
- Endpoint: `https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openrouter`

## Testing and Quality Assurance

Currently, the project doesn't have formal testing, linting, or type checking commands configured. When implementing these:

1. Test each command with all global flags (`--verbose`, `--json`, `--yaml`, `--debug`, `--quiet`, `--silent`)
2. Verify JSON/YAML output is valid and complete
3. Check animations work properly and respect quiet/silent
4. Ensure error cases are handled gracefully
5. Test auto-loading by adding/removing command files
6. Verify AI integrations handle API errors gracefully

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

## Extension Guidelines

### New Commands

- Follow existing patterns for consistency
- Use `BaseCommand` inheritance
- Implement proper error handling
- Add comprehensive help text with emojis
- Test with all global flag combinations
- Use utility functions for common operations

### AI-Powered Commands

- Use `get_openai_client()` for AI integration
- Configure caching based on use case (disable for dynamic content)
- Implement structured outputs with JSON schemas
- Handle API errors gracefully with try/except blocks
- Add verbose logging for debugging AI interactions
- Consider rate limits and implement appropriate delays

### Performance Considerations

- Early return for `config.silent` to skip processing
- Lazy loading of heavy operations
- Efficient Rich component usage
- Minimal overhead for quiet mode
- Configure AI Gateway caching for repeated queries
- Use appropriate retry strategies for AI calls

## Command Development Checklist

When creating a new command:

- [ ] Created new file in `commands/` directory
- [ ] Inherited from `BaseCommand`
- [ ] Implemented `register_command` static method
- [ ] Implemented `execute` static method
- [ ] Added proper type hints throughout
- [ ] Used utility functions appropriately
- [ ] Respected global configuration flags
- [ ] Added comprehensive help text with emoji
- [ ] Included error handling
- [ ] Tested with all global flags
- [ ] Verified auto-loading works
- [ ] For AI commands: configured gateway settings appropriately
- [ ] Updated documentation if needed
