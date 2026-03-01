# Rules.py Documentation

## Overview

`rules.py` is a utility script that merges multiple MDC (Markdown with Components) files from the `_cursor/rules` directory into a single, organised Markdown document. The script automatically reformats YAML front matter as plain Markdown, fixes structural issues, and generates a unified rules file suitable for use with Cursor IDE.

## Description

This script processes a collection of MDC files containing development rules and conventions. It:

- Extracts and parses YAML front matter from individual MDC files
- Converts front matter metadata into readable Markdown format
- Consolidates all files into a single `rules-merged.md` document
- Ensures Markdown compliance by fixing code blocks and heading levels
- Optionally formats the output using Prettier for consistency
- Supports custom user rules that take precedence over standard rules

The resulting merged document is sorted alphabetically by title and includes a timestamp indicating when it was generated.

## Usage Instructions

### Basic Usage

```plaintext
python3 rules.py
```

This command will:

1. Search for all `.mdc` files in the `_cursor/rules` directory
2. Process each file to extract and reformat content
3. Generate `rules-merged.md` in the current working directory
4. Automatically format the output with Prettier (if available)

### With Verbose Output

```plaintext
python3 rules.py --verbose
```

or

```plaintext
python3 rules.py -v
```

When the `--verbose` flag is used, the script prints detailed information about:

- Commands being executed
- Files being processed
- Dependency checks
- Prettier formatting operations

## CLI Arguments and Flags

### `-v`, `--verbose`

**Type:** Boolean flag (no value required)

**Description:** Enables verbose output mode. The script will print detailed diagnostic information about its operations, including executed commands, file processing steps, and dependency checks.

**Example:**

```plaintext
python3 rules.py -v
```

## Input and Output Files

### Input Directory

- **Location:** `_cursor/rules/`
- **Format:** MDC files with `.mdc` extension
- **Structure:** May contain optional YAML front matter between `---` delimiters

### Optional User Rules File

- **Location:** `rules.md` (in the current working directory)
- **Format:** Plain Markdown
- **Behaviour:** If present, content from this file is included at the top of the merged output, before standard rules

### Output File

- **Location:** `rules-merged.md` (generated in the current working directory)
- **Format:** Markdown
- **Contents:** Merged and reformatted content from all input files

## Dependencies

### Required

- **Python 3.6+** - Core language requirement
- **PyYAML** - For parsing YAML front matter. The script automatically installs this if not present.
- **types-PyYAML** - Type stubs for PyYAML, used for type checking. The script automatically installs this if not present.

### Optional

- **Prettier** - A code formatter used to format the final Markdown output. If not available on the system PATH, the script skips formatting with a warning message and continues successfully.

### Automatic Dependency Management

The script includes automatic dependency management:

- Checks if `types-PyYAML` is installed via `pip show`
- Automatically installs `pyyaml` and `types-PyYAML` if missing
- Attempts installation once; if it fails, the script exits with an error message

## Notable Implementation Details

### YAML Front Matter Processing

The script uses a regex pattern to identify YAML front matter blocks:

```plaintext
---
title: Example Rule
priority: high
---
```

The front matter is then converted to Markdown format:

- The `title` field becomes an H2 heading (`##`)
- Other fields are converted to bold key-value pairs (e.g., `**priority**: high`)

### Markdown Compliance Fixes

The script automatically corrects several common Markdown issues:

1. **Multiple Top-Level Headings (MD025):** Converts all H1 headings (`#`) in content to H2 (`##`) to ensure only one H1 exists
2. **Fenced Code Blocks (MD040):** Adds `plaintext` language specifier to code blocks without language specification
3. **Emphasis vs. Headers (MD036):** Uses proper H2 headings instead of emphasis for metadata

### Slug Generation

The `create_valid_slug()` function creates URL-safe slugs from text:

- Converts to lowercase
- Replaces spaces with hyphens
- Removes non-alphanumeric characters (except underscores and hyphens)
- Collapses multiple consecutive hyphens

This function is defined but not used in the current implementation.

### File Sorting

Processed files are sorted alphabetically by their title in case-insensitive order, ensuring consistent organisation regardless of the original file names.

### Title Extraction

Titles are determined by the following priority:

1. If a YAML `title` field exists in front matter, that value is used
2. Otherwise, the first H1 heading in the content is used
3. If neither exists, "Untitled Section" is assigned

### Error Handling

The script gracefully handles various error conditions:

- Missing input directories (reports and returns without error)
- Unreadable files (logs error and continues processing other files)
- YAML parsing errors (logs error but preserves file content)
- Missing Prettier (skips formatting and continues)
- Failed dependency installation (exits with error message)

### Prettier Integration

If Prettier is available on the system PATH:

- The script automatically formats the output Markdown file
- Formatting failures are logged but do not prevent script completion
- Absence of Prettier is treated as non-critical

## Example Workflow

Given an `_cursor/rules` directory with the following files:

```
_cursor/rules/
├── authentication.mdc
├── code-style.mdc
└── documentation.mdc
```

And an optional `rules.md` file with custom high-priority rules:

```markdown
# High Priority Rules

Always run security checks before deployment.
```

Running `python3 rules.py` will:

1. Process each `.mdc` file
2. Sort by title
3. Generate `rules-merged.md` containing:
   - High Priority Rules section (from `rules.md`)
   - Standard Rules header
   - Generation timestamp
   - All processed rules sorted alphabetically
   - Each section separated by horizontal rules (`---`)

## Exit Codes

- **0:** Successful execution
- **1:** Failed to install or import PyYAML dependency

## Security Considerations

The script uses `subprocess.run()` with trusted, constrained inputs only:

- Subprocess calls use fixed command lists built from safe sources
- No shell interpretation is used
- User input is not passed to shell commands

The script includes Bandit security scan exemptions (`nosec B404, B603`) for subprocess usage, which are appropriate given the controlled nature of the inputs.
