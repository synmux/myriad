# XMP Mover

## Overview

XMP Mover is a Python utility that identifies XMP (Extensible Metadata Platform) files that have associated companion files with the same base name but different file extensions. Once identified, it automatically moves both the XMP files and their companions to a dedicated `with-xmp` directory for better organisation and file management.

This utility is particularly useful for photographers and content creators who work with XMP sidecar files, which store metadata alongside their corresponding image or document files.

## Description

The tool performs the following operations:

1. **Recursive Directory Scanning**: Traverses the current working directory and all subdirectories to identify files.
2. **Companion File Detection**: Groups files by their base name (filename without extension) and identifies XMP files that have non-XMP companions.
3. **Organised Movement**: Moves matching XMP and companion files to a `with-xmp` subdirectory.
4. **Error Handling**: Gracefully handles file operation errors and prevents overwriting existing files.
5. **Progress Reporting**: Displays real-time progress bars and detailed logging throughout the operation.
6. **Dry Run Support**: Allows users to simulate the operation before actually moving files.

## Usage Instructions

### Basic Usage

To run the tool with default settings, simply execute it from the directory containing the files you wish to process:

```bash
python3 xmp-mover.py
```

This will:

- Scan all files in the current directory and subdirectories
- Create a `with-xmp` directory (if it doesn't already exist)
- Move all XMP files and their companion files to the `with-xmp` directory

### Example Workflow

Given a directory structure like:

```
project/
├── photo.jpg
├── photo.xmp
├── document.pdf
├── document.xmp
└── standalone.txt
```

Running the tool will produce:

```
project/
├── standalone.txt
└── with-xmp/
    ├── photo.jpg
    ├── photo.xmp
    ├── document.pdf
    └── document.xmp
```

### Command-Line Arguments

#### `--xmp-only`

**Type**: Flag (boolean)
**Default**: Not set (moves both XMP and companion files)

When specified, moves only the XMP files whilst leaving their companion files in their original locations.

**Example**:

```bash
python3 xmp-mover.py --xmp-only
```

#### `--dry-run`

**Type**: Flag (boolean)
**Default**: Not set (performs actual file operations)

Simulates the entire operation without actually moving any files. This is useful for previewing what changes would occur before running the tool in production mode.

**Example**:

```bash
python3 xmp-mover.py --dry-run
```

#### Combined Arguments

You can combine both flags:

```bash
python3 xmp-mover.py --xmp-only --dry-run
```

## Dependencies

The utility requires the following Python packages:

- **Python 3.7+**: The script uses type hints and modern Python features.
- **Rich**: A library for rich text and beautiful formatting in the terminal. Required for:
  - Progress bars with real-time updates
  - Formatted table output for summary statistics
  - Styled console logging with colour support

### Installation

If Rich is not already installed, install it using pip:

```bash
pip install rich
```

## Notable Implementation Details

### Architecture

The script employs a two-pass scanning approach:

1. **Pre-scan Pass**: Counts the total number of files in the directory tree to provide accurate progress bar percentages.
2. **Main Scanning Pass**: Processes files, groups them by base name, identifies companions, and handles movement operations.

### File Grouping Strategy

The utility uses a `defaultdict` to efficiently group files by their base name (without extension). This allows quick identification of which XMP files have companion files with the same base name.

### Logging and Output

The tool implements a dual-output logging strategy:

- **Console Output**: Rich-formatted progress bars and summary tables are sent to standard output (stdout).
- **File Logging**: Detailed operation logs are written to `xmp_move_log.txt` in the current working directory.
- **Logging Handler**: Uses Rich's `RichHandler` for styled console output with timestamps and traceback support.

### Safety Features

- **Existing File Protection**: Skips moving files if the destination path already exists, preventing accidental overwrites.
- **Dry Run Mode**: Allows safe preview of operations without modifying the filesystem.
- **Hidden File Handling**: Ignores files with base names starting with a dot (hidden files).
- **Target Directory Exclusion**: Automatically skips the `with-xmp` directory during subsequent scans to avoid re-processing.
- **Error Tracking**: Maintains an error counter to report how many file operations failed during execution.

### Extension Handling

- Extensions are normalised to lowercase for reliable comparison.
- The utility looks for files with the exact extension `.xmp` (case-insensitive).
- All file types are supported as companion files; only the presence of XMP files triggers movement.

### Progress Indication

The progress bar displays:

- Percentage of files processed
- Time remaining (estimated)
- Time elapsed

This information is cleared from the terminal upon completion to avoid cluttering the output.

### Summary Report

After processing completes, the tool displays a formatted table containing:

- Processing mode (Dry Run or Actual Run)
- Total files scanned
- Number of files moved (or would be moved in dry run mode)
- Number of errors encountered (with colour coding: red for errors, green for success)

### Error Handling

The tool catches the following exception types during file operations:

- `IOError`: Input/output errors
- `OSError`: Operating system errors
- `shutil.Error`: Errors from the shutil module

All errors are logged with details about which file caused the issue, allowing users to investigate and retry if necessary.

### Exit Codes

- **0**: Successful completion
- **1**: Fatal error (e.g., target directory creation failure, unexpected exception)

The utility also catches `KeyboardInterrupt` to handle user interruption gracefully, logging the interruption before exiting.

## Log File

A detailed log file named `xmp_move_log.txt` is created in the current working directory. This file contains:

- Timestamp of each operation
- Log level (INFO, WARNING, ERROR)
- Detailed message describing the operation

Review this file for troubleshooting if operations fail or behave unexpectedly.
