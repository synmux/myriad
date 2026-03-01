# Sidecar Orphan Finder

## Overview

`orphans.py` is a command-line utility designed to identify and manage orphaned sidecar files—files that exist without corresponding media files. This is particularly useful for photo and media libraries where sidecar files (such as XMP metadata sidecars) accumulate over time without their associated images or media.

A sidecar file is an auxiliary file that accompanies a primary media file. For example, an XMP file (`photo.xmp`) is a sidecar that stores metadata for an image file (`photo.jpg`). When the primary media file is deleted or moved, the sidecar file may remain behind, creating "orphans". This utility helps find and optionally remove these orphaned files.

## Features

- **Flexible sidecar detection**: Find orphaned files with any extension (defaults to `.xmp`)
- **Comprehensive file scanning**: Uses the system `find` command for efficient recursive directory traversal
- **Visual progress indication**: Rich, colour-coded output with progress bars showing operation status
- **Safe deletion**: Includes a dry-run mode to preview changes before taking action
- **Detailed reporting**: Generates informative tables and summaries of all operations
- **Robust error handling**: Graceful error reporting with detailed exception information

## Installation

### Prerequisites

- Python 3.6 or higher
- Unix-like system with `find` command available (Linux, macOS, BSD)
- `rich` Python library for formatting and progress bars

### Install Dependencies

Install the required Python package using pip:

```bash
pip install rich
```

### Setup

1. Ensure the script has execute permissions:

```bash
chmod +x orphans.py
```

2. Optionally, place the script in your PATH or create a symbolic link for system-wide access.

## Usage

### Basic Syntax

```bash
./orphans.py [DIRECTORY] [OPTIONS]
```

### Examples

#### List orphaned files in the current directory

```bash
./orphans.py
```

#### List orphaned files in a specific directory

```bash
./orphans.py /path/to/photos
```

#### Preview what would be deleted (dry-run mode)

```bash
./orphans.py /path/to/photos --dry-run
```

#### Delete all orphaned sidecar files

```bash
./orphans.py /path/to/photos --delete
```

#### Find orphaned files with a different sidecar extension

```bash
./orphans.py /path/to/photos --extension jpg
```

#### Combine options

```bash
./orphans.py /path/to/media --extension dng --dry-run
```

## Command-Line Arguments

### Positional Arguments

| Argument    | Description                                        | Default                 |
| ----------- | -------------------------------------------------- | ----------------------- |
| `DIRECTORY` | The directory to search for orphaned sidecar files | `.` (current directory) |

### Optional Arguments

| Flag          | Short Form | Description                                                   | Default |
| ------------- | ---------- | ------------------------------------------------------------- | ------- |
| `--dry-run`   | —          | Display what would be deleted without actually removing files | `false` |
| `--delete`    | —          | Delete orphaned sidecar files (use with caution)              | `false` |
| `--extension` | `-e`       | Specify the sidecar file extension to search for              | `xmp`   |
| `--help`      | `-h`       | Display the help message and exit                             | —       |

### Detailed Option Descriptions

#### `--dry-run`

Runs the utility in preview mode. The tool will:

- Scan the directory for orphaned files
- Display a list of files that would be deleted
- Make no changes to the file system

This is recommended before using `--delete` to ensure you're targeting the correct files.

#### `--delete`

Enables deletion mode. The tool will:

- Identify orphaned sidecar files
- Permanently remove them from the file system
- Display confirmation messages with the count of deleted files

**Warning**: This operation is irreversible. Always verify using `--dry-run` first.

#### `--extension` / `-e`

Specifies the sidecar file extension to search for. Examples:

- `xmp` (default): Adobe XMP metadata sidecars
- `dng`: Adobe DNG (Digital Negative) sidecar files
- `pp3`: RawTherapee profile files
- `thm`: Thumbnail sidecar files

## Dependencies

### Python Packages

- **rich** (>= 10.0.0): Provides colour-coded terminal output, progress bars, and formatted panels

### System Commands

- **find**: Unix utility for recursive file system searching (included on macOS, Linux, and BSD systems)

### Python Standard Library

- `argparse`: Command-line argument parsing
- `os`: File system operations
- `subprocess`: Execution of system commands
- `sys`: System-specific operations
- `time`: Execution time measurement
- `typing`: Type hints for function definitions

## Implementation Details

### File Discovery Strategy

The utility uses the `find` command via `subprocess` for efficient file discovery:

1. **Sidecar files**: Found using the pattern `*.{extension}` (e.g., `*.xmp`)
2. **Media files**: Located by finding all files that don't match the sidecar pattern
3. **Hidden files**: Explicitly excluded (those beginning with `.`)

This approach is more efficient than Python's native file system traversal for large directories.

### Orphan Detection Algorithm

The detection process works as follows:

1. **Index media files**: Creates a set of base filenames (without extensions) for all non-sidecar files
2. **Check sidecars**: For each sidecar file, extracts its base filename and checks if a corresponding media file exists
3. **Identify orphans**: Any sidecar file whose base name doesn't match a media file base name is marked as orphaned

**Example**:

- Media files: `photo1.jpg`, `photo2.png`, `document.pdf`
- Sidecar files: `photo1.xmp`, `photo2.xmp`, `photo3.xmp`, `photo4.xmp`
- Orphaned sidecars: `photo3.xmp`, `photo4.xmp` (no corresponding media files)

### Base Filename Extraction

The `get_base_filename()` function:

- Extracts the filename from a full path
- Removes the file extension to create a base name
- Handles both sidecar and media files uniformly

This allows matching `photo.jpg` with `photo.xmp` regardless of different extensions.

### Progress Reporting

The utility uses the Rich library to provide:

- **Status spinners**: Animated feedback during file discovery
- **Progress bars**: Visual representation of work completion with percentage and count
- **Coloured panels**: Organised, easy-to-read output sections
- **Execution summary**: Final report with statistics and timing information

### Error Handling

The application includes robust error handling:

1. **Keyboard interruption**: Gracefully handles user cancellation (Ctrl+C) with an appropriate message
2. **File deletion errors**: Attempts to delete each file individually, reporting any errors without stopping the entire operation
3. **Rich tracebacks**: Uses Rich's traceback handler to provide detailed error information in a readable format
4. **Exit codes**: Returns exit code `1` on error or cancellation, `0` on success

### Performance Considerations

- **Subprocess-based discovery**: The `find` command is faster than Python's native file traversal for large directories
- **In-memory processing**: Once files are discovered, all operations occur in memory, reducing system I/O
- **Progress feedback**: Progress bars provide reassurance during long-running operations on large directories

## Security Considerations

- **Deletion is irreversible**: Files deleted with the `--delete` flag cannot be recovered. Use `--dry-run` first.
- **Path traversal**: The utility operates on absolute paths resolved from input, preventing directory traversal attacks
- **Hidden files excluded**: Files and directories beginning with `.` are excluded from scanning, avoiding system directories
- **Subprocess execution**: Uses `subprocess.run()` with `capture_output=True` and explicit command lists to prevent shell injection

## Output Examples

### Sample Output - Detection Only

```
🔍 Sidecar Orphan Finder
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Target Directory: /home/user/Photos                              ┃
┃ Sidecar Extension: .xmp                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📊 File Statistics
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Found:                                                           ┃
┃ Sidecar Files (.xmp): 245                                       ┃
┃ Media Files: 240                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Found 5 orphaned .xmp files
┏━━━━━━━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status                 ┃ File Path                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 📄 Orphaned           │ /home/user/Photos/deleted_1.xmp   │
│ 📄 Orphaned           │ /home/user/Photos/deleted_2.xmp   │
│ 📄 Orphaned           │ /home/user/Photos/old_file.xmp    │
└───────────────────────┴────────────────────────────────────┘
```

### Sample Output - Dry Run Mode

```
Found 5 orphaned .xmp files
Showing orphaned files | Would delete these files (DRY RUN)

🗑️ Would have deleted 5 orphaned .xmp files
```

### Sample Output - Deletion Complete

```
✅ Deleted 5 orphaned .xmp files
```

## Troubleshooting

### Issue: "No such file or directory"

**Cause**: The specified directory does not exist.

**Solution**: Verify the directory path and ensure it exists before running the utility.

### Issue: No files are found

**Cause**: The directory may not contain any sidecar files with the specified extension.

**Solution**: Verify the correct sidecar extension using the `--extension` flag. For example, if you have `.dng` files instead of `.xmp`, run:

```bash
./orphans.py /path/to/directory --extension dng
```

### Issue: Permission denied error during deletion

**Cause**: The user running the script lacks write permissions for the target directory.

**Solution**: Ensure you have write permissions:

```bash
ls -ld /path/to/directory
chmod u+w /path/to/directory  # if needed
```

### Issue: Operation takes a long time on large directories

**Cause**: The directory contains a very large number of files.

**Solution**: This is expected behaviour. The progress bar shows the operation is continuing. You can monitor progress and adjust your approach by:

- Running on a smaller subdirectory first
- Using `--dry-run` initially to preview results without deletion overhead

## Contributing

To report bugs or suggest improvements, please provide:

- A description of the issue
- Steps to reproduce the problem
- Expected vs. actual behaviour
- Your operating system and Python version

## Licence

This utility is provided as-is. Ensure you understand the risks of file deletion before using the `--delete` flag.

## Version History

- **1.0**: Initial release with XMP orphan detection and deletion capabilities
