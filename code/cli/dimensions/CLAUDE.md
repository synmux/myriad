# Dimensions CLI Tool - AI Assistant Documentation

## Overview

The Dimensions CLI tool is a comprehensive Python application for analyzing image dimensions in directories. It's part of the myriad monorepo and provides fast scanning, beautiful terminal output, and comprehensive statistics about image sizes in collections.

## Architecture

### Project Structure

```
code/cli/dimensions/
├── README.md               # User documentation
├── CLAUDE.md              # This file - AI assistant documentation
├── PROMPT.md              # Original implementation prompt
├── .gitignore             # Git ignore patterns
├── src/
│   └── dimensions/
│       ├── __init__.py    # Package initialization with version info
│       ├── __main__.py    # CLI entry point
│       ├── cli.py         # Click CLI interface and main logic
│       ├── scanner.py     # Directory scanning and file discovery
│       ├── processor.py   # Image processing with Pillow
│       ├── formatter.py   # Output formatting (text/json/yaml)
│       ├── organizer.py   # File organization (move/copy/symlink)
│       └── utils.py       # Shared utilities and helpers
└── tests/
    ├── __init__.py        # Test package
    ├── test_scanner.py    # Scanner module tests
    └── test_utils.py      # Utility function tests
```

### Key Components

#### 1. Scanner Module (`scanner.py`)
- **Purpose**: Recursively discovers image files in directories
- **Key Classes**: `DirectoryScanner`
- **Features**: 
  - Recursive directory traversal
  - Image file filtering by extension
  - Error handling for permissions/access issues
  - Progress tracking for large directories

#### 2. Processor Module (`processor.py`)
- **Purpose**: Extracts dimensions from image files using Pillow
- **Key Classes**: `ImageProcessor`, `ImageInfo`, `DimensionStats`
- **Features**:
  - Multi-threaded processing support
  - HEIC format support via pillow-heif
  - Dimension caching to avoid re-processing
  - Comprehensive error handling for corrupted images

#### 3. Formatter Module (`formatter.py`)
- **Purpose**: Outputs results in multiple formats
- **Key Classes**: `OutputFormatter`
- **Features**:
  - Rich terminal tables with colors
  - JSON and YAML export
  - Summary statistics generation
  - File output support

#### 4. Organizer Module (`organizer.py`)
- **Purpose**: Moves, copies, or symlinks files by dimensions
- **Key Classes**: `FileOrganizer`, `OperationType`
- **Features**:
  - Three operation modes (move/copy/symlink)
  - Dry-run preview functionality
  - Filename conflict resolution
  - Progress tracking and error reporting

#### 5. CLI Module (`cli.py`)
- **Purpose**: Click-based command-line interface
- **Features**:
  - Comprehensive option validation
  - Progress bars using tqdm
  - Structured logging with structlog
  - Integration of all components

### Data Flow

1. **Scanning Phase**: `DirectoryScanner` finds all image files recursively
2. **Processing Phase**: `ImageProcessor` extracts dimensions (optionally multi-threaded)
3. **Organization Phase** (optional): `FileOrganizer` moves/copies/symlinks files
4. **Output Phase**: `OutputFormatter` displays results in chosen format

## Dependencies

### Core Dependencies
- `click>=8.1.8`: CLI framework for command-line interface
- `rich>=14.0.0`: Terminal formatting and beautiful tables
- `tqdm>=4.67.0`: Progress bars for long-running operations
- `pillow>=11.0.0`: Image processing library for reading dimensions
- `pillow-heif>=1.0.0`: HEIC format support extension
- `pyyaml>=6.0.2`: YAML output format support
- `orjson>=3.10.20`: Fast JSON serialization
- `structlog>=25.1.0`: Structured logging framework

### Development Dependencies
- `pytest>=8.4.0`: Testing framework
- `pytest-cov>=6.1.1`: Coverage reporting
- `black>=25.1.0`: Code formatting
- `ruff>=0.11.13`: Fast Python linter
- `mypy>=1.16.0`: Static type checking

## Usage Patterns

### Basic Analysis
```bash
# Analyze current directory
dimensions

# Analyze specific directory with progress
dimensions /path/to/photos --threads 4
```

### Output Formats
```bash
# Rich text output (default)
dimensions /photos

# JSON export
dimensions /photos --format json --output results.json

# YAML export  
dimensions /photos --format yaml --output results.yaml
```

### File Organization
```bash
# Move files to dimension folders
dimensions /photos --move /organized --dry-run  # Preview first
dimensions /photos --move /organized             # Actually move

# Copy files instead of moving
dimensions /photos --copy /backup_by_size

# Create symlinks
dimensions /photos --symlink /links_by_dimensions
```

### Filtering and Sorting
```bash
# Show only common dimensions
dimensions /photos --min-count 10 --max-results 20

# Sort by dimensions instead of count
dimensions /photos --sort dimensions
```

## Error Handling

The tool implements comprehensive error handling:

1. **File Access Errors**: Permission denied, file not found
2. **Image Processing Errors**: Corrupted files, unsupported formats
3. **Directory Errors**: Missing directories, permission issues
4. **Organization Errors**: Write permissions, disk space, filename conflicts

All errors are logged using structlog and don't stop the overall process.

## Performance Considerations

### Multi-threading
- Default: Single-threaded processing
- Configurable via `--threads` parameter
- Optimal thread count depends on I/O vs CPU bottlenecks
- Progress tracking works correctly in multi-threaded mode

### Memory Usage
- Only reads image headers, not full image data
- Implements dimension caching to avoid re-processing
- Batch processing for large directories
- Memory-efficient file iteration

### Large Collections
- Progress bars for user feedback
- Batch processing to reduce memory overhead
- Configurable result limits (`--max-results`)
- Filtering options to focus on relevant data

## Testing Strategy

### Unit Tests
- `test_scanner.py`: Directory scanning functionality
- `test_utils.py`: Utility functions and helpers
- Mock-based testing for error conditions
- Temporary directory fixtures for file operations

### Integration Testing
- End-to-end CLI testing with Click's test runner
- Real image file processing tests
- Multi-format output validation
- File organization operation testing

### Test Coverage
- Comprehensive coverage of all modules
- Error condition testing
- Edge case validation
- Performance regression testing

## Configuration and Extension

### Adding New Image Formats
1. Update `SUPPORTED_EXTENSIONS` in `utils.py`
2. Ensure Pillow supports the format or add appropriate plugin
3. Add test cases for the new format
4. Update documentation

### Adding New Output Formats
1. Extend `OutputFormatter` class with new format method
2. Add format choice to CLI options
3. Implement data serialization for the format
4. Add comprehensive tests

### Adding New File Operations
1. Extend `OperationType` enum in `organizer.py`
2. Implement operation logic in `FileOrganizer`
3. Add CLI option and validation
4. Add tests for the new operation

## Troubleshooting Guide

### Common Issues

1. **No images found**
   - Check directory path exists and is readable
   - Verify supported image formats in directory
   - Check file permissions

2. **Slow processing**
   - Use `--threads` for multi-threading
   - Check disk I/O performance
   - Consider filtering options

3. **Permission errors**
   - Ensure read access to source directories
   - Ensure write access for file operations
   - Check target directory permissions

4. **Memory issues**
   - Tool should use minimal memory (header-only reading)
   - Check for corrupted images causing memory leaks
   - Use filtering to reduce dataset size

### Debug Mode
```bash
# Enable detailed logging
dimensions /path --log-level DEBUG

# Disable progress bars for cleaner logs
dimensions /path --log-level DEBUG --no-progress
```

## Integration Notes

### Monorepo Integration
- Package is part of the myriad project
- Dependencies are shared in root `pyproject.toml`
- Console script entry point: `dimensions = "dimensions.__main__:main"`
- Uses `uv` for dependency management

### CI/CD Considerations
- Tests can be run with `uv run pytest code/cli/dimensions/tests/`
- Linting with `uv run ruff check code/cli/dimensions/`
- Type checking with `uv run mypy code/cli/dimensions/src/`
- Code formatting with `uv run black code/cli/dimensions/`

## Future Enhancements

### Potential Features
1. **Database Support**: Store results in SQLite/PostgreSQL
2. **Web Interface**: Flask/FastAPI web UI
3. **Image Metadata**: Extract EXIF data, creation dates
4. **Duplicate Detection**: Find similar/identical images
5. **Batch Operations**: Process multiple directories
6. **Configuration Files**: YAML/JSON config support
7. **Plugin System**: Extensible architecture for custom processors

### Performance Optimizations
1. **Async I/O**: Use asyncio for file operations
2. **Result Caching**: Persistent cache for large collections
3. **Parallel Scanning**: Multi-threaded directory traversal
4. **Memory Mapping**: For very large file operations

This documentation provides a comprehensive understanding of the dimensions CLI tool for AI assistants working with the codebase.