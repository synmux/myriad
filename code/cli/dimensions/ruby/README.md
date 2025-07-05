# Dimensions CLI Tool - Ruby Implementation

A powerful Ruby CLI tool for analyzing image dimensions in directories. This is a Ruby port of the original Python implementation, providing fast scanning, beautiful terminal output, and comprehensive statistics about image sizes in your collections.

## Features

- **Fast recursive directory scanning** for image files
- **Multi-threaded processing** for improved performance
- **Rich terminal output** with tables and colors
- **Multiple export formats** (JSON, YAML, pretty text)
- **File organization** by dimensions (move, copy, symlink)
- **Comprehensive filtering and sorting** options
- **Dry-run mode** for safe operation previews

## Installation

1. Install Ruby (3.0 or higher recommended)
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Ensure ImageMagick is installed on your system (required by mini_magick):

   ```bash
   # macOS
   brew install imagemagick

   # Ubuntu/Debian
   apt-get install imagemagick

   # CentOS/RHEL
   yum install ImageMagick
   ```

## Usage

### Basic Analysis

```bash
# Analyze current directory
./bin/dimensions

# Analyze specific directory
./bin/dimensions /path/to/photos

# Analyze multiple directories
./bin/dimensions /photos1 /photos2
```

### Multi-threaded Processing

```bash
# Use 4 threads for faster processing
./bin/dimensions /photos --threads 4
```

### Output Formats

```bash
# Rich text output (default)
./bin/dimensions /photos

# JSON export
./bin/dimensions /photos --format json --output results.json

# YAML export
./bin/dimensions /photos --format yaml --output results.yaml
```

### File Organization

```bash
# Preview moving files to dimension folders (dry run)
./bin/dimensions /photos --move /organized --dry-run

# Actually move files
./bin/dimensions /photos --move /organized

# Copy files instead of moving
./bin/dimensions /photos --copy /backup_by_size

# Create symlinks
./bin/dimensions /photos --symlink /links_by_dimensions
```

### Filtering and Sorting

```bash
# Show only dimensions with 10+ images, limit to 20 results
./bin/dimensions /photos --min-count 10 --max-results 20

# Sort by dimensions instead of count
./bin/dimensions /photos --sort dimensions
```

### Logging and Debug

```bash
# Enable debug logging
./bin/dimensions /photos --log-level DEBUG

# Disable progress bars for cleaner logs
./bin/dimensions /photos --no-progress
```

## Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- BMP (`.bmp`)
- TIFF (`.tiff`, `.tif`)
- WebP (`.webp`)
- HEIC/HEIF (`.heic`, `.heif`, `.heics`, `.heifs`, `.hif`)
- DNG (`.dng`)

## Command Line Options

| Option          | Description                                 | Default   |
| --------------- | ------------------------------------------- | --------- |
| `--format`      | Output format (text, json, yaml)            | text      |
| `--sort`        | Sort by count or dimensions                 | count     |
| `--min-count`   | Show only dimensions with N+ images         | 1         |
| `--max-results` | Limit number of results                     | unlimited |
| `--threads`     | Number of processing threads                | 1         |
| `--log-level`   | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO      |
| `--output`      | Save output to file                         | stdout    |
| `--no-progress` | Disable progress bars                       | false     |
| `--move`        | Move files to dimension directories         | -         |
| `--copy`        | Copy files to dimension directories         | -         |
| `--symlink`     | Create symlinks by dimensions               | -         |
| `--dry-run`     | Preview operations without executing        | false     |

## Architecture

### Core Components

- **Scanner** (`scanner.rb`): Recursively discovers image files
- **Processor** (`processor.rb`): Extracts dimensions using mini_magick
- **Formatter** (`formatter.rb`): Outputs results in multiple formats
- **Organizer** (`organizer.rb`): Moves/copies/symlinks files by dimensions
- **CLI** (`cli.rb`): Commander-based command-line interface
- **Utils** (`utils.rb`): Shared utilities and helpers

### Dependencies

- **commander** - CLI framework
- **mini_magick** - Fast image processing via ImageMagick
- **tty-progressbar** - Progress bars
- **tty-table** - Terminal tables
- **pastel** - Terminal colors
- **parallel** - Multi-threading support
- **json/psych** - JSON and YAML support

## Development

### Running Tests

```bash
bundle exec rspec
```

### Code Quality

```bash
# Linting
bundle exec rubocop

# Auto-fix issues
bundle exec rubocop -a
```

## Performance Considerations

- **Multi-threading**: Use `--threads` option for I/O bound workloads
- **Memory efficiency**: Only reads image headers, not full image data
- **Progress tracking**: Real-time feedback for long operations
- **Filtering**: Use `--min-count` and `--max-results` to focus on relevant data

## Error Handling

The tool provides comprehensive error handling for:

- File access permissions
- Corrupted image files
- Missing directories
- Write permission issues
- Filename conflicts during organization

All errors are logged appropriately and don't stop the overall process.

## Differences from Python Version

While maintaining functional parity, this Ruby implementation:

- Uses **mini_magick** instead of Pillow for image processing
- Uses **Commander** instead of Click for CLI
- Uses **TTY gems** instead of Rich for terminal UI
- Uses **Parallel** gem for multi-threading
- Follows Ruby idioms and conventions

## Contributing

This is part of the larger myriad monorepo. Please follow the established patterns and conventions when contributing.
