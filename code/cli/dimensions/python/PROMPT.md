# `PROMPT.md`

Create a Python CLI application that analyzes image dimensions in a directory. The application should:

## Core Functionality

- Scan all image files (jpg, jpeg, png, gif, bmp, tiff, webp, heic) in the selected directory recursively
- Collect and count unique width × height dimension combinations
- Handle corrupted/unreadable images gracefully with warnings

## Project Structure

Use modern Python project structure with `uv`:

- pyproject.toml with proper metadata and dependencies
- src/dimensions/ package structure
- CLI entry point in **main**.py
- Separate modules for: scanning, processing, formatting, CLI
- Type hints throughout (use Python 3.13+ features)
- Add .gitignore for Python projects
- You are in a monorepo.
  - Your code should live in `code/cli/dimensions/`, including Markdown documentation.
    - For example, the `src/` directory should be at `code/cli/dimensions/src/`.
    - For example, the `README.md` file should be at `code/cli/dimensions/README.md`.
  - The `pyproject.toml` file is in the root directory.
    - Add to it at will, but don't break the other projects using it.

## Dependencies & Tools

- Use `uv` for dependency management
- `click` for CLI framework with proper help text
- `tqdm` for progress bars
- `Pillow` for image reading
- `rich` for beautiful terminal output (tables, colors)
- `pyyaml` for YAML output
- `orjson` for fast JSON handling
- `concurrent.futures` with ThreadPoolExecutor for multithread
- `pathlib` for path operations
- `structlog` for structured logging

## CLI Interface

```plaintext
dimensions [OPTIONS] [PATH]

Options:
  --format [text|json|yaml]  Output format (default: text)
  --sort [count|dimensions]  Sort results by count or dimensions (default: count desc)
  --min-count INTEGER        Only show dimensions with at least N images
  --max-results INTEGER      Limit number of results shown
  --threads INTEGER          Select number of processing threads
  --log-level [DEBUG|INFO|WARNING|ERROR]
  --help                    Show this message and exit
```

## Output Requirements

- Live progress information, warnings, and errors to STDERR using structlog
  - `tqdm` progress bar on STDERR too if possible
- Results to STDOUT in chosen format
  - Always display text output. If `json` or `yaml` is enabled, write the text output to STDERR and the structured data to STDOUT.
  - If neither `json` nor `yaml` are enabled, write the text to STDOUT.
- Text format: Use rich.table with columns [Dimensions, Count, Percentage, Sample Files]
- JSON format: {"dimensions": [{"width": X, "height": Y, "count": N, "percentage": P}], "summary": {...}}
- YAML format: Similar structure to JSON but in YAML
- Include summary statistics to STDERR: total images, unique dimensions, most common dimension

## Implementation Details

- Pre-scan phase to count total images for accurate progress
- Batch processing to minimize thread overhead
- Cache dimension results to avoid re-reading same files
- Handle edge cases: empty directories, permission errors, symbolic links
- Memory-efficient: don't load full images, just read headers
- Progress bar should show: current file, files/sec, ETA, dimension count
- Use parallel processing if `--threads` is specified.
  - Default to a single threads if `--threads` is not specified.
- Add support for HEIC images, pulling in libraries and searching the Web for their documentation as necessary.
  - `pillow-heif` is a good option - `pillow` does not support HEIC by default.
- Support file operations:
  - Move files to directories by dimensions (e.g., `1000x1000/`), `--move [DIR]`
  - Copy files to directories by dimensions (e.g., `1000x1000/`), `--copy [DIR]`
  - Create symlinks to files by dimensions (e.g., `1000x1000/`), `--symlink [DIR]`
  - These three options are mutually exclusive, only one can be specified.

## Code Quality

- Research all libraries - search the Web thoroughly for documentation and examples.
- Use latest stable versions of all dependencies
- Follow PEP 8 and use black for formatting
  - Add black to dev dependencies
- Add comprehensive docstrings
- Include basic unit tests for core functions
- Add README.md with usage examples

Start by researching the latest best practices for the main libraries you'll use, then create the project structure.

## When done (FINAL TASK, WAITS UNTIL THE VERY END)

- Make sure that all dependencies are at their latest versions.
  - If anything needs to be updated, update it. That includes major versions.
  - Ideally, we'll be using latest versions from the start, but you sometimes add older versions.
  - Search the Web for documentation to understand the migration and any breaking changes.
- Systematically check all the code and tests for bugs.
  - Fix any issues you find.
- Ensure all documentation is up to date, including docstrings and Markdown files.
- Make any other improvements you feel should be made, in order to make the CLI tool better.

## README

This was previously implemented, and was then deleted by accident. I was able to recover this prompt and the README. It may be of assistance.

README begins:

---

A powerful Python CLI tool that analyzes image dimensions in directories. Built with modern Python practices, it provides fast scanning, beautiful terminal output, and comprehensive statistics about image sizes in your collections.

### Features

- 🚀 **Fast Scanning**: Efficient directory traversal with optional multi-threading
- 📊 **Rich Statistics**: Detailed analysis of image dimensions with percentages and file samples
- 🎨 **Beautiful Output**: Rich terminal tables with colors and formatting
- 📋 **Multiple Formats**: Export results as JSON, YAML, or formatted text
- 📁 **File Organization**: Move, copy, or symlink images into folders by dimensions (e.g., `1920x1080/`)
- 🔄 **Dry Run Support**: Preview file operations before executing them
- 🔧 **Robust Processing**: Graceful error handling for corrupted or inaccessible files
- 📈 **Progress Tracking**: Real-time progress bars with processing statistics
- 🖼️ **Wide Format Support**: JPEG, PNG, GIF, BMP, TIFF, WebP, HEIC, and more

### Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- TIFF (`.tiff`, `.tif`)
- WebP (`.webp`)
- HEIC/HEIF (`.heic`, `.heif`, `.heics`, `.heifs`, `.hif`) - _Requires pillow-heif_

### Installation

#### Using uv (Recommended)

```bash
## Clone the repository
git clone https://github.com/example/dimensions.git
cd dimensions

## Install with uv
uv pip install -e .
```

#### Using pip

```bash
## Clone the repository
git clone https://github.com/example/dimensions.git
cd dimensions

## Install dependencies
pip install -e .
```

#### Development Installation

```bash
## Install with development dependencies
uv pip install -e ".[dev]"

## Or with pip
pip install -e ".[dev]"
```

### Quick Start

```bash
## Analyze current directory
dimensions

## Analyze specific directory
dimensions /path/to/images

## Use multiple threads for faster processing
dimensions /large/photo/collection --threads 4

## Export results as JSON
dimensions /photos --format json --output results.json

## Show only dimensions with 10+ images
dimensions /images --min-count 10 --max-results 20

## Organize images by moving them to dimension folders
dimensions /photos --move /organized_photos

## Preview organization without moving files
dimensions /images --copy /backup --dry-run
```

### Usage

#### Basic Command

```bash
dimensions [OPTIONS] [PATH]
```

#### Options

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
## Analyze current directory with default settings
dimensions

## Analyze specific directory
dimensions ~/Pictures/Photos
```

#### Multi-threaded Processing

```bash
## Use 4 threads for faster processing of large collections
dimensions /media/photos --threads 4

## Maximum threads (useful for very large collections)
dimensions /archive/images --threads 8
```

#### Filtering and Sorting

```bash
## Show only dimensions with 5 or more images
dimensions /photos --min-count 5

## Limit to top 10 results
dimensions /images --max-results 10

## Sort by dimensions instead of count
dimensions /pictures --sort dimensions

## Combine filters
dimensions /gallery --min-count 3 --max-results 15 --sort count
```

#### Output Formats

```bash
## Default text output with Rich formatting
dimensions /photos

## JSON output to stdout
dimensions /images --format json

## YAML output to stdout
dimensions /pictures --format yaml

## Save JSON to file
dimensions /photos --format json --output analysis.json

## Save YAML to file
dimensions /images --format yaml --output report.yaml
```

#### File Organization

```bash
## Move images to directories by dimensions
dimensions /photos --move /organized_photos

## Copy images to directories by dimensions
dimensions /images --copy /backup_by_size

## Create symlinks organized by dimensions
dimensions /photos --symlink /links_by_dimensions

## Preview operations before executing
dimensions /images --move /organized --dry-run

## Combine with filtering for specific dimensions
dimensions /photos --move /organized --min-count 5 --max-results 10
```

#### Advanced Usage

```bash
## Detailed logging for troubleshooting
dimensions /problematic/images --log-level DEBUG

## Quiet processing without progress bars
dimensions /images --no-progress --log-level ERROR

## Process large collection with optimized settings
dimensions /massive/archive --threads 6 --min-count 10 --no-progress
```

### Output Examples

#### Text Output (Default)

```plaintext
                    Summary Statistics
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric            ┃ Value                               ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Images      │ 1,234                               │
│ Unique Dimensions │ 15                                  │
│ Failed Files      │ 2                                   │
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

#### JSON Output

```json
{
  "summary": {
    "total_images": 1234,
    "unique_dimensions": 15,
    "failed_files": 2,
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

#### YAML Output

```yaml
summary:
  total_images: 1234
  unique_dimensions: 15
  failed_files: 2
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

### Development

#### Setup Development Environment

```bash
## Clone repository
git clone https://github.com/example/dimensions.git
cd dimensions

## Install development dependencies
uv pip install -e ".[dev]"

## Run tests
pytest

## Run tests with coverage
pytest --cov=src/dimensions

## Format code
black src/ tests/

## Run linting
ruff check src/ tests/
```

#### Project File Structure

```plaintext
dimensions/
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
├── .gitignore             # Git ignore patterns
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
    └── test_scanner.py    # Unit tests
```

#### Running Tests

```bash
## Run all tests
pytest

## Run with verbose output
pytest -v

## Run specific test file
pytest tests/test_scanner.py

## Run with coverage report
pytest --cov=src/dimensions --cov-report=html
```

### Performance Tips

1. **Use Multiple Threads**: For large image collections, use `--threads 4` or higher
2. **Filter Results**: Use `--min-count` to focus on significant dimensions
3. **Limit Output**: Use `--max-results` for large collections
4. **Disable Progress**: Use `--no-progress` for better performance in scripts

### Error Handling

The tool gracefully handles various error conditions:

- **Corrupted Images**: Logged as warnings, don't stop processing
- **Permission Errors**: Clearly reported with file paths
- **Unsupported Formats**: Skipped silently
- **Network Drives**: May be slower, use fewer threads

### Troubleshooting

#### Common Issues

**No images found**: Check that the directory contains supported image formats and you have read permissions.

**Slow processing**: Use multiple threads (`--threads 4`) for large collections.

**Memory usage**: The tool only reads image headers, not full images, so memory usage should be minimal.

**Permission errors**: Ensure you have read access to all directories and files.

#### Debug Mode

```bash
## Enable debug logging for detailed information
dimensions /path/to/images --log-level DEBUG
```

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Changelog

#### v0.2.0 (File Organization)

- **NEW**: File organization options (`--move`, `--copy`, `--symlink`)
- **NEW**: Organize images into directories by dimensions (e.g., `1920x1080/`)
- **NEW**: Dry-run support for previewing operations
- **NEW**: Full HEIC/HEIF image support with pillow-heif
- **NEW**: Comprehensive file operation error handling
- **ENHANCED**: CLI validation for mutually exclusive options
- **ENHANCED**: Improved directory creation and permission handling

#### v0.1.0 (Initial Release)

- Basic directory scanning and image processing
- Support for major image formats
- Rich terminal output with tables
- JSON and YAML export options
- Multi-threaded processing
- Comprehensive error handling
- Progress tracking with tqdm

---
