# Bump Dependency Manager

## Overview

Bump is a sophisticated command-line utility for automating dependency version updates across multiple repositories. It intelligently manages dependencies across JavaScript/TypeScript (npm), Python (PyPI), and Ruby (RubyGems) projects whilst respecting semantic versioning rules and providing comprehensive visual feedback through a beautiful terminal user interface.

## Description

Bump is designed to simplify the complex task of keeping project dependencies up to date across large repository structures. Rather than manually checking and updating each dependency in each project, Bump automatically:

1. Discovers all repositories in a target directory structure
2. Identifies dependencies across multiple package managers
3. Queries package registries for available updates
4. Applies intelligent version bumping based on semantic versioning rules
5. Updates lockfiles and commits changes to version control

The utility is particularly useful for teams maintaining multiple related projects or monorepo-style structures, allowing centralised dependency management with minimal manual intervention.

## Features

- **Multi-Repository Support**: Processes all repositories under a base directory or targets a specific repository
- **Multi-Language Support**: Handles dependencies from JavaScript/TypeScript, Python, and Ruby projects
- **Smart Version Bumping**: Applies version bumping based on semantic versioning rules with configurable safety constraints
- **Efficient Batch Processing**: Batches API calls to package registries with retry logic to avoid rate limiting
- **Beautiful Terminal UI**: Provides detailed progress information with colour-coded output using spinners and formatted boxes
- **Dry-Run Mode**: Preview changes before applying them to the codebase
- **Git Integration**: Automatically syncs repositories, commits changes, and optionally pushes to remote
- **Flexible Workflow Control**: Fine-grained control over which steps to execute

## Installation

Bump is built with Bun and requires Bun to be installed on your system. Install Bun from [https://bun.sh](https://bun.sh).

## Usage

### Basic Usage

```bash
bump
```

This command processes all repositories discovered in the default directory (`/Users/dave/src/github.com/daveio/`) and checks for available dependency updates.

### Target Specific Repository

```bash
bump my-project
```

Processes only the specified repository instead of all repositories in the base directory.

### Dry Run

```bash
bump --dry-run
```

Performs all checks and displays what would be updated without making any actual changes to files or repositories.

## Command-Line Arguments and Flags

### Arguments

- `[repo]` (optional): Target a specific repository name. If omitted, all repositories in the base directory are processed.

### Options

#### `--dry-run`

- **Type**: Boolean flag
- **Default**: `false`
- **Description**: Makes no changes and only prints what would be updated. Useful for previewing changes before application.

#### `--unsafe`

- **Type**: Boolean flag
- **Default**: `false`
- **Description**: Overrides version safety rules to bump all version levels (including major versions) to the latest available. By default, major version bumps are skipped unless this flag is specified.

#### `--no-pull`

- **Type**: Boolean flag (inverted)
- **Default**: Git pull is enabled
- **Description**: Skips git fetch and pull operations. Use this if you want to work with the current state of repositories without syncing from remote.

#### `--no-install`

- **Type**: Boolean flag (inverted)
- **Default**: Installation is enabled
- **Description**: Skips dependency installation and lockfile update steps. Useful when you only want to update version specifications without refreshing lockfiles.

#### `--no-commit`

- **Type**: Boolean flag (inverted)
- **Default**: Commit is enabled
- **Description**: Skips the git commit step. Useful when you want to review and commit changes manually.

#### `--no-push`

- **Type**: Boolean flag (inverted)
- **Default**: Push is enabled
- **Description**: Skips the git push step. Use this to commit changes locally without pushing to remote.

## Supported File Types and Package Managers

### JavaScript/TypeScript (npm)

- **Files**: `package.json`
- **Sections Processed**: `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies`
- **Registry**: npm Registry

### Python (PyPI)

- **Files**: `pyproject.toml`
- **Formats Supported**: Poetry (`[tool.poetry.dependencies]`) and PEP 621 (`[project]`)
- **Registry**: PyPI

### Ruby (RubyGems)

- **Files**: `Gemfile`, `*.gemspec`
- **Registry**: RubyGems

## Semantic Versioning Rules

Bump applies intelligent version bumping based on semantic versioning comparison:

- **Patch Updates** (e.g., 1.2.3 → 1.2.4): Applied automatically
- **Minor Updates** (e.g., 1.2.3 → 1.3.0): Applied automatically
- **Major Updates** (e.g., 1.2.3 → 2.0.0): Skipped by default unless `--unsafe` flag is specified

This approach ensures stability by preventing potentially breaking changes unless explicitly requested.

## Workflow

The utility executes the following steps in order (unless skipped via flags):

1. **Repository Discovery**: Identifies all git repositories in the target directory
2. **Dependency Reading**: Scans all repositories for dependencies across supported package managers
3. **Git Synchronisation** (if `--pull`): Fetches and pulls the latest changes from remote repositories
4. **Update Checking**: Queries package registries for available versions with intelligent batching and retry logic
5. **Update Application**: Applies updates to dependency files according to versioning rules
6. **Lockfile Updates** (if `--install`): Runs package manager commands to update lockfiles
7. **Git Operations** (if `--commit`): Commits changes and optionally pushes to remote (if `--push`)
8. **Summary Report**: Displays a detailed summary of all changes grouped by dependency or repository

## Dependencies

Bump relies on the following Node.js packages:

### Core Dependencies

- **`@iarna/toml`**: TOML parsing for Python `pyproject.toml` files
- **`axios`**: HTTP client for querying package registries
- **`boxen`**: Terminal box drawing for formatted output
- **`chalk`**: Terminal colour and styling
- **`commander`**: Command-line interface and argument parsing
- **`js-yaml`**: YAML parsing (included for future extensibility)
- **`ora`**: Terminal spinners for progress indication
- **`semver`**: Semantic versioning comparison and validation

### Node.js Built-ins

- `child_process`: For executing shell commands (git operations)
- `fs/promises`: For file system operations
- `path`: For path manipulation and normalisation
- `util.promisify`: For converting callback-based functions to Promise-based

## Notable Implementation Details

### Efficient Batch Processing

The utility implements sophisticated batch processing to minimise API calls and avoid rate limiting:

- **npm**: Processes up to 20 packages per batch
- **PyPI**: Processes up to 10 packages per batch (stricter rate limits)
- **RubyGems**: Processes up to 10 packages per batch

All three package managers are queried in parallel for maximum efficiency.

### Dependency Deduplication

When processing multiple repositories, the utility deduplicates dependencies before querying registries. This ensures that if the same package is used across multiple projects, the registry is only queried once, then results are distributed to all projects using that dependency.

### Path Traversal Protection

Repository paths are sanitised to prevent path traversal attacks when specifying target repositories. The `..` sequences are removed and path separators are normalised.

### Comprehensive Error Handling

Each phase of the process includes error handling with informative output. If a step fails for a specific repository or dependency, processing continues for others with the error logged to the console.

### File I/O Optimisation

Dependencies are grouped by file path before updates are applied, minimising file I/O operations by processing all dependencies in a single file together.

### Visual Progress Reporting

The utility uses `ora` spinners and `chalk` colouring to provide clear, real-time feedback:

- Red symbols (`✗`) indicate major version updates
- Yellow symbols (`△`) indicate minor version updates
- Green symbols (`✓`) indicate patch version updates

## Execution Summary

After processing, Bump displays a comprehensive summary that can be grouped by either dependency or repository, showing:

- Current version and latest available version for each update
- Type of version bump (patch/minor/major)
- Which repositories are affected
- Total execution time

## Configuration

Bump uses a hardcoded base directory of `/Users/dave/src/github.com/daveio/` for repository discovery. To modify this, edit the `discoverRepositories` function in the source code.

## Runtime Requirements

- **Bun**: v1.0 or later (as indicated by the shebang: `#!/usr/bin/env bun`)
- **Node.js Compatibility**: The script uses Node.js built-in modules and is compatible with Node.js versions supported by Bun
- **Git**: Required for `--pull`, `--commit`, and `--push` operations
- **Package Managers**: `npm`, `pip`/`poetry`, and `gem` are required to be installed for their respective dependency types when using `--install`

## Examples

### Check all dependencies in all repositories

```bash
bump
```

### Preview changes without making any modifications

```bash
bump --dry-run
```

### Update a specific repository including major versions

```bash
bump --unsafe my-project
```

### Update dependencies but skip git operations

```bash
bump --no-pull --no-commit --no-push
```

### Update dependencies and lockfiles but skip git integration

```bash
bump --no-commit --no-push
```

### Process a specific repository with all safety measures but no automatic push

```bash
bump --no-push my-project
```

## Exit Codes

- **0**: Success
- **1**: Fatal error (e.g., invalid repository, missing base directory)

## Notes

- The utility maintains a detailed execution log in the console output
- All updates respect the semantic versioning constraints unless `--unsafe` is specified
- Git operations require appropriate repository access and permissions
- The utility creates comprehensive output using colour and formatting; ensure your terminal supports ANSI colours for optimal experience
