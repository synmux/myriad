# Pin: GitHub Actions Workflow Pinning Utility

## Overview

`pin` is a TypeScript utility that automatically updates GitHub Actions workflow files to pin action references to their latest commit SHAs. This ensures reproducible workflows and improves security by replacing mutable version references (such as major version tags) with immutable commit hashes.

## Purpose

GitHub Actions typically reference actions using version tags or major version numbers (e.g., `actions/checkout@v3` or `my-org/my-action@main`). These references can change when new versions are released, potentially introducing breaking changes or security vulnerabilities into your workflows.

This utility scans all GitHub Actions used across one or more repositories and updates them to pin against the specific commit SHA of the latest commit on the default branch. This provides:

- **Reproducibility**: Workflows behave identically across all executions
- **Security**: Prevents unexpected updates from upstream action repositories
- **Control**: Centralised management of action versions across multiple repositories
- **Safety**: Automatic backups are created before any modifications

## Installation & Requirements

### Prerequisites

- **Bun Runtime**: The script is designed to run with Bun (see shebang line: `#!/usr/bin/env -S bun --enable-source-maps`)
- **GitHub CLI**: The `gh` command-line tool must be installed and authenticated
- **Node.js APIs**: Uses Node.js built-in modules (child_process, fs, path, util)

### Dependencies

The utility requires the following npm packages:

- `commander`: Command-line interface framework
- `js-yaml`: YAML parsing and serialisation

## Usage

### Basic Syntax

```bash
pin [directory]
```

### Arguments

| Argument    | Required | Description                                                                                                                           |
| ----------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `directory` | No       | Path to a specific git repository to process. If omitted, the utility scans `/Users/dave/src/github.com/daveio` for all repositories. |

### Examples

**Process all repositories in the default directory:**

```bash
pin
```

**Process a specific repository:**

```bash
pin /path/to/my-repo
```

**Process a repository in the current directory:**

```bash
pin .
```

## How It Works

### Processing Flow

1. **Repository Discovery**: If no specific directory is provided, the utility scans the default path for all git repositories (directories containing a `.git` folder).

2. **Workflow File Analysis**: For each repository, the utility locates all GitHub Actions workflow files (`.github/workflows/*.{yml,yaml}`).

3. **Action Reference Extraction**: Workflow files are parsed to identify all GitHub Actions references in the `uses` field. The utility extracts:
   - Docker references (skipped)
   - Local actions (skipped)
   - Published GitHub Actions with version/commit references

4. **Repository Metadata Caching**: The utility queries GitHub's GraphQL API to fetch metadata for all unique repositories referenced in workflows:
   - Default branch name
   - Latest commit SHA on that branch
   - Results are cached in memory to avoid redundant API calls

5. **Workflow File Updating**: Each workflow file is updated by:
   - Replacing the action reference version with the latest commit SHA
   - Preserving all other YAML structure and properties
   - Creating timestamped backups before modification

6. **Summary Report**: After processing, a comprehensive summary is printed showing all changes, repositories processed, and any errors encountered.

### Batch Processing & API Optimisation

The utility uses batch processing to efficiently query GitHub's API:

- Batches of up to 50 repositories are queried per GraphQL request to avoid query size limits
- If GraphQL requests fail, the utility automatically falls back to individual REST API calls
- This ensures reliable operation even with large numbers of action references

### Backup Strategy

All original workflow files are backed up before modification:

- Backups are stored in `~/.actions-backups/{TIMESTAMP}/`
- The timestamp format is `YYYY-MM-DD_HH-MM-SS` for easy identification
- Each repository's directory structure is preserved in the backup
- This allows quick rollback if needed

## Implementation Details

### Key Data Structures

```typescript
interface ActionUpdate {
  actionPath: string; // e.g., "owner/repo/action"
  oldRef: string; // Original version/commit reference
  newRef: string; // New commit SHA
}

interface WorkflowUpdate {
  filePath: string; // Full path to workflow file
  relativePath: string; // Path relative to repository root
  updates: ActionUpdate[];
}

interface RepoUpdate {
  repoName: string;
  workflowUpdates: WorkflowUpdate[];
}

interface ProcessingSummary {
  repoUpdates: RepoUpdate[];
  errors: string[];
  totalReposProcessed: number;
  totalFilesProcessed: number;
  totalActionsUpdated: number;
}
```

### Core Functions

#### `findRepositories(rootDir: string): string[]`

Recursively searches a directory for git repositories and returns an array of absolute paths.

#### `extractUniqueRepos(repositoriesToProcess: string[]): Set<string>`

Parses all workflow files in given repositories and returns a set of unique action repositories referenced (in `owner/repo` format).

#### `buildRepoCache(uniqueRepos: Set<string>): Promise<GitHubRepoCache>`

Fetches metadata for all unique repositories using GitHub's GraphQL API with fallback to REST API. Returns a cache mapping repository names to their default branch and latest commit SHA.

#### `processRepository(repoName, repoPath, backupDir, summary, repoCache): Promise<RepoUpdate>`

Processes all workflow files in a single repository, updating action references and creating backups.

#### `processWorkflowFile(filePath, repoPath, backupDir, repoCache): Promise<WorkflowUpdate | null>`

Updates a single workflow file:

- Creates a backup before modification
- Parses the YAML structure recursively
- Updates all action references to their latest commit SHAs
- Writes the updated file back to disk

#### `getTimestamp(): string`

Generates a timestamp string in `YYYY-MM-DD_HH-MM-SS` format for backup directory naming.

### YAML Handling

The utility:

- Preserves YAML structure using `js-yaml` library
- Uses `lineWidth: -1` to prevent automatic line wrapping
- Disables YAML reference tags (`noRefs: true`) to ensure clean output
- Uses double-quote string formatting for consistency

### GitHub API Integration

The utility leverages:

- **GraphQL API**: Efficiently queries multiple repositories in a single batch request
- **GitHub CLI Authentication**: Uses `gh auth token` to retrieve the authenticated session token
- **REST API Fallback**: If GraphQL queries fail, falls back to individual `gh` CLI commands
- **Automatic Error Handling**: Continues processing if individual repositories fail

### Reference Parsing

The utility correctly identifies and processes:

- Standard GitHub Actions: `owner/repo@version` → pinned to commit SHA
- Action Subdirectories: `owner/repo/action-dir@version` → pinned with path preserved
- Multiple Actions per Workflow: All are updated in a single pass
- Nested YAML Structures: Recursively processes complex workflow definitions

The utility correctly skips:

- Local actions: `./path/to/local/action`
- Docker images: `docker://image:tag`
- Invalid references: Malformed action paths
- Unavailable repositories: Logs warnings and continues processing

## Output & Logging

The utility provides detailed console output throughout execution:

- Discovery phase: Shows repositories found and scan locations
- Caching phase: Displays batch processing progress and GraphQL query results
- Update phase: Logs each action as it is pinned
- Summary phase: Comprehensive report of all changes and any errors

### Sample Output

```
🔍 Finding repositories and updating GitHub Action workflows...
🔍 Scanning for repositories in: /Users/dave/src/github.com/daveio
Found 3 repository(ies) to process

🔍 Fetching metadata for 5 unique repositories using GraphQL...
  📦 Processing 1 batch(es) of repositories...
  🔄 Processing batch 1/1 (5 repositories)...
    ✓ Cached owner/action-one: main@a1b2c3d4e5f6...
    ✓ Cached owner/action-two: main@f6e5d4c3b2a1...
  📊 Batch 1 completed: 5/5 repositories cached

📁 Processing repository: my-repo
  Found 2 workflow files
  📌 Pinned owner/action-one from v1 to a1b2c3d4e5f6...
  ✅ Updated .github/workflows/ci.yml with 2 action references

📊 Summary of GitHub Action Updates
===============================
Repositories processed: 3
Workflow files processed: 6
Action references updated: 8
Backup location: /Users/dave/.actions-backups/2026-03-01_14-30-45
```

## Limitations & Notes

1. **Default Directory**: The hard-coded default directory is `/Users/dave/src/github.com/daveio`. For general use, this should be customised or made configurable via environment variables.

2. **GitHub API Rate Limits**: Large numbers of repositories may approach GitHub API rate limits. The batching mechanism helps mitigate this.

3. **Authentication**: Requires `gh` CLI to be authenticated with appropriate permissions to access all referenced repositories.

4. **Concurrency**: The utility has a `_MAX_CONCURRENCY` constant set to 5 (currently unused in the implementation) that could be utilised for parallel repository processing in future versions.

5. **YAML Modifications**: The utility modifies YAML files which may reformat them. Comments and formatting may change, though the semantic content is preserved.

## Error Handling

The utility handles errors gracefully:

- **Missing Repositories**: Logs errors and continues processing
- **Failed API Calls**: Automatically falls back to REST API for batch failures
- **Inaccessible Repositories**: Logs warnings and skips unavailable actions
- **Invalid Workflow Files**: Logs errors and continues with other files
- **Fatal Errors**: Exits with error code 1 and displays error message

All errors are collected in the summary report and displayed at the end of execution.

## Security Considerations

- **Credentials**: Uses GitHub CLI for authentication, credentials are handled securely by `gh`
- **Backups**: Complete backups are automatically created before modifications
- **Read-Only by Default**: Only creates backups; doesn't delete or permanently modify files until after backup creation
- **API Token Handling**: Token is retrieved from `gh` auth and used only for API requests

## Exit Codes

- **0**: Successful completion
- **1**: Fatal error or invalid input (directory not found, not a git repository, etc.)
