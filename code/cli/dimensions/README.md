# Dimensions CLI Tool

A powerful Python CLI tool that analyzes image dimensions in directories. Built with modern Python practices, it provides fast scanning, beautiful terminal output, and comprehensive statistics about image sizes in your collections.

## Features

- 🚀 **Fast Scanning**: Efficient directory traversal with optional multi-threading
- 📊 **Rich Statistics**: Detailed analysis of image dimensions with percentages and file samples
- 🎨 **Beautiful Output**: Rich terminal tables with colors and formatting
- 📋 **Multiple Formats**: Export results as JSON, YAML, or formatted text
- 📁 **File Organization**: Move, copy, or symlink images into folders by dimensions (e.g., `1920x1080/`)
- 🔄 **Dry Run Support**: Preview file operations before executing them
- 🔧 **Robust Processing**: Graceful error handling for corrupted or inaccessible files
- 📈 **Progress Tracking**: Real-time progress bars with processing statistics
- 🖼️ **Wide Format Support**: JPEG, PNG, GIF, BMP, TIFF, WebP, HEIC, and more

## Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- TIFF (`.tiff`, `.tif`)
- WebP (`.webp`)
- HEIC/HEIF (`.heic`, `.heif`, `.heics`, `.heifs`, `.hif`) - _Requires pillow-heif_

## Installation

This tool is part of the myriad monorepo. To install and use:

### Using uv (Recommended)

```bash
# Install the monorepo dependencies
uv sync

# Run the tool directly
uv run python -m dimensions [OPTIONS] [PATH]
```

### Using the console script

```bash
# After installation, you can use the console script
dimensions [OPTIONS] [PATH]
```

### Development Installation

```bash
# Install with development dependencies
uv sync --group dev

# Run tests
uv run pytest code/cli/dimensions/tests/

# Run linting
uv run ruff check code/cli/dimensions/
```

## Quick Start

```bash
# Analyze current directory
dimensions

# Analyze specific directory
dimensions /path/to/images

# Use multiple threads for faster processing
dimensions /large/photo/collection --threads 4

# Export results as JSON
dimensions /photos --format json --output results.json

# Show only dimensions with 10+ images
dimensions /images --min-count 10 --max-results 20

# Organize images by moving them to dimension folders
dimensions /photos --move /organized_photos

# Preview organization without moving files
dimensions /images --copy /backup --dry-run
```

## Usage

### Basic Command

```bash
dimensions [OPTIONS] [PATH]
```

### Options

| Option           | Type   | Default | Description                                        |
| ---------------- | ------ | ------- | -------------------------------------------------- |
| `--format`       | choice | `text`  | Output format: `text`, `json`, or `yaml`           |
| `--sort`         | choice | `count` | Sort by `count` (descending) or `dimensions`       |
| `--min-count`    | int    | `1`     | Only show dimensions with at least N images        |
| `--max-results`  | int    | None    | Limit number of results shown                      |
| `--threads`      | int    | `1`     | Number of processing threads                       |
| `--log-level`    | choice | `INFO`  | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--no-progress`  | flag   | False   | Disable progress bars                              |
| `--output`, `-o` | path   | None    | Save output to file                                |
| `--move`         | path   | None    | Move images to directories by dimensions           |
| `--copy`         | path   | None    | Copy images to directories by dimensions           |
| `--symlink`      | path   | None    | Create symlinks to images by dimensions            |
| `--dry-run`      | flag   | False   | Preview operations without executing               |
| `--help`, `-h`   | flag   | False   | Show help message                                  |
| `--version`      | flag   | False   | Show version                                       |

### Examples

#### Basic Analysis

```bash
# Analyze current directory with default settings
dimensions

# Analyze specific directory
dimensions ~/Pictures/Photos
```

#### Multi-threaded Processing

```bash
# Use 4 threads for faster processing of large collections
dimensions /media/photos --threads 4

# Maximum threads (useful for very large collections)
dimensions /archive/images --threads 8
```

#### Filtering and Sorting

```bash
# Show only dimensions with 5 or more images
dimensions /photos --min-count 5

# Limit to top 10 results
dimensions /images --max-results 10

# Sort by dimensions instead of count
dimensions /pictures --sort dimensions

# Combine filters
dimensions /gallery --min-count 3 --max-results 15 --sort count
```

#### Output Formats

```bash
# Default text output with Rich formatting
dimensions /photos

# JSON output to stdout
dimensions /images --format json

# YAML output to stdout
dimensions /pictures --format yaml

# Save JSON to file
dimensions /photos --format json --output analysis.json

# Save YAML to file
dimensions /images --format yaml --output report.yaml
```

#### File Organization

```bash
# Move images to directories by dimensions
dimensions /photos --move /organized_photos

# Copy images to directories by dimensions
dimensions /images --copy /backup_by_size

# Create symlinks organized by dimensions
dimensions /photos --symlink /links_by_dimensions

# Preview operations before executing
dimensions /images --move /organized --dry-run

# Combine with filtering for specific dimensions
dimensions /photos --move /organized --min-count 5 --max-results 10
```

#### Advanced Usage

```bash
# Detailed logging for troubleshooting
dimensions /problematic/images --log-level DEBUG

# Quiet processing without progress bars
dimensions /images --no-progress --log-level ERROR

# Process large collection with optimized settings
dimensions /massive/archive --threads 6 --min-count 10 --no-progress
```

## Output Examples

### Text Output (Default)

```plaintext
                    Summary Statistics
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric            ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Images      │ 1,234                               │
│ Unique Dimensions │ 15                                  │
│ Total Size        │ 2.3 GB                              │
│ Most Common       │ 1920×1080 (456 images)             │
└───────────────────┴─────────────────────────────────────┘

        Image Dimensions Analysis - 1,234 images
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dimensions    ┃ Count ┃ Percentage  ┃ Total Size ┃ Sample Files                         ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1920×1080     │   456 │      37.0%  │    1.2 GB  │ photo_001.jpg, IMG_5432.jpg (+454)  │
│ 4032×3024     │   234 │      19.0%  │  756.2 MB  │ DSC01234.jpg, image_789.jpg (+232)  │
│ 1080×1080     │   189 │      15.3%  │  234.5 MB  │ square_01.png, social_pic.jpg (+187)│
│ 3840×2160     │    98 │       7.9%  │  445.1 MB  │ 4k_photo.jpg, wallpaper.png (+96)   │
│ 1280×720      │    67 │       5.4%  │   89.3 MB  │ hd_image.jpg, screenshot.png (+65)  │
└───────────────┴───────┴─────────────┴────────────┴──────────────────────────────────────┘
```

### JSON Output

```json
{
  "summary": {
    "total_images": 1234,
    "unique_dimensions": 15,
    "total_size": "2.3 GB",
    "most_common_dimension": "1920×1080",
    "most_common_count": 456
  },
  "dimensions": [
    {
      "width": 1920,
      "height": 1080,
      "dimensions": "1920×1080",
      "count": 456,
      "percentage": 37.0,
      "total_size_bytes": 1288490188,
      "total_size": "1.2 GB",
      "sample_files": ["/photos/photo_001.jpg", "/photos/IMG_5432.jpg", "/photos/vacation_pic.jpg"]
    }
  ]
}
```

### YAML Output

```yaml
summary:
  total_images: 1234
  unique_dimensions: 15
  total_size: 2.3 GB
  most_common_dimension: 1920×1080
  most_common_count: 456
dimensions:
  - width: 1920
    height: 1080
    dimensions: 1920×1080
    count: 456
    percentage: 37.0
    total_size_bytes: 1288490188
    total_size: 1.2 GB
    sample_files:
      - /photos/photo_001.jpg
      - /photos/IMG_5432.jpg
      - /photos/vacation_pic.jpg
```

## Development

### Project File Structure

```plaintext
code/cli/dimensions/
├── README.md               # This file
├── src/
│   └── dimensions/
│       ├── __init__.py    # Package initialization
│       ├── __main__.py    # CLI entry point
│       ├── cli.py         # Click CLI interface
│       ├── scanner.py     # Directory scanning logic
│       ├── processor.py   # Image processing with Pillow
│       ├── formatter.py   # Output formatting (text/json/yaml)
│       ├── organizer.py   # File organization (move/copy/symlink)
│       └── utils.py       # Shared utilities
└── tests/
    ├── __init__.py
    ├── test_scanner.py    # Scanner tests
    └── test_utils.py      # Utility tests
```

### Running Tests

```bash
# Run all tests
uv run pytest code/cli/dimensions/tests/

# Run with verbose output
uv run pytest -v code/cli/dimensions/tests/

# Run specific test file
uv run pytest code/cli/dimensions/tests/test_scanner.py

# Run with coverage report
uv run pytest --cov=dimensions --cov-report=html code/cli/dimensions/tests/
```

### Code Quality

```bash
# Format code
uv run black code/cli/dimensions/

# Run linting
uv run ruff check code/cli/dimensions/

# Type checking
uv run mypy code/cli/dimensions/src/
```

## Performance Tips

1. **Use Multiple Threads**: For large image collections, use `--threads 4` or higher
2. **Filter Results**: Use `--min-count` to focus on significant dimensions
3. **Limit Output**: Use `--max-results` for large collections
4. **Disable Progress**: Use `--no-progress` for better performance in scripts

## Error Handling

The tool gracefully handles various error conditions:

- **Corrupted Images**: Logged as warnings, don't stop processing
- **Permission Errors**: Clearly reported with file paths
- **Unsupported Formats**: Skipped silently
- **Network Drives**: May be slower, use fewer threads

## Troubleshooting

### Common Issues

**No images found**: Check that the directory contains supported image formats and you have read permissions.

**Slow processing**: Use multiple threads (`--threads 4`) for large collections.

**Memory usage**: The tool only reads image headers, not full images, so memory usage should be minimal.

**Permission errors**: Ensure you have read access to all directories and files.

### Debug Mode

```bash
# Enable debug logging for detailed information
dimensions /path/to/images --log-level DEBUG
```

## Dependencies

- Python 3.13+
- click: CLI framework
- rich: Terminal formatting
- tqdm: Progress bars
- Pillow: Image processing
- pillow-heif: HEIC support
- pyyaml: YAML output
- orjson: Fast JSON handling
- structlog: Structured logging

## License

This project is part of the myriad monorepo and is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes in the `code/cli/dimensions/` directory
4. Add tests for new functionality
5. Ensure all tests pass (`uv run pytest`)
6. Run code quality checks (`uv run ruff check`)
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request