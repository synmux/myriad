# clone-repos.bash

## Description

`clone-repos.bash` is a utility script for batch cloning and synchronising GitHub repositories. It reads a newline-delimited list of repository names from standard input, then clones or updates each repository in parallel. For each repository, the script performs a comprehensive fetch and pull operation to ensure all branches, tags, and submodules are up-to-date.

## Usage

### Basic invocation

```bash
cat repository-list.txt | ./clone-repos.bash
```

### Input format

The script expects repositories in the format `username/repository-name`, one per line:

```plaintext
kubernetes/kubernetes
torvalds/linux
golang/go
```

Each entry will be cloned to a directory named after the repository (e.g., `kubernetes`, `linux`, `go`).

### Example

```bash
# Clone multiple repositories
echo -e "nodejs/node\npython/cpython\nrust-lang/rust" | ./clone-repos.bash

# Clone repositories from a file
cat repos.txt | ./clone-repos.bash
```

## Operations performed

For each repository, the script performs the following actions:

1. **Clone or update detection**: Checks whether the repository directory already exists locally.

2. **For new repositories**:
   - Clones the repository from GitHub using HTTPS: `https://github.com/username/repository.git`
   - Fetches all remote data with pruning and tag management
   - Pulls all branches with rebase strategy

3. **For existing repositories**:
   - Fetches all remote data with pruning and tag management
   - Pulls all branches with rebase strategy

### Git operations in detail

Each repository receives the following git operations:

```bash
git fetch --all --prune --tags --prune-tags --recurse-submodules=yes
git pull --all --prune --rebase
```

- `--all`: Fetch from or pull to all remotes
- `--prune`: Remove remote-tracking references that no longer exist on the remote
- `--tags`: Fetch or include tags
- `--prune-tags`: Remove local tags that no longer exist on the remote
- `--recurse-submodules=yes`: Recursively fetch/pull submodules
- `--rebase`: Use rebase instead of merge when pulling

## Dependencies

- **bash**: Version 4.0 or later (for associative arrays and advanced features)
- **git**: Must be installed and available in the system PATH
- **xargs**: Standard Unix utility for parallel command execution
- **curl** or similar: Implicitly required by `git clone` over HTTPS

## Implementation details

### Parallelisation

The script uses `xargs` with the `-P 16` flag to process up to 16 repositories concurrently. This provides significant performance improvement when cloning or updating multiple repositories simultaneously.

```bash
xargs -P 16 -I{} bash -c "process_repo {}"
```

To adjust the level of parallelism, modify the `-P 16` parameter:

- `-P 4`: Lower concurrency (useful on resource-constrained systems)
- `-P 32`: Higher concurrency (for systems with many CPU cores and good network bandwidth)

### Function export

The `process_repo` function is exported using `export -f` to make it available to the subshells spawned by `xargs`.

### Directory handling

The script extracts the repository name from the full `username/repository` path using `basename`, which ensures that each repository is cloned into a directory matching its name, regardless of the depth of the input path.

### Error handling

The script uses subshell operations (`(...)`) and short-circuit evaluation (`&&`) to ensure that:

- If a `cd` operation fails, the script returns without executing subsequent commands
- If `git fetch` fails, `git pull` is not executed
- Errors in one repository do not halt processing of other repositories

### Output

The script provides basic console feedback:

- `"Cloning ${repo}"`: Printed when a new repository is cloned
- `"Updating ${repo}"`: Printed when an existing repository is updated

## Exit status

The script does not explicitly return an exit code. Exit status will reflect the result of the final `xargs` command. Individual repository errors are reported to the console but do not halt processing of subsequent repositories.

## Notes

- The script clones repositories using HTTPS. If SSH access is required, modify the clone URL from `https://github.com/` to `git@github.com:`.
- The script performs a rebase-based pull strategy, which maintains a linear history but may require conflict resolution if local changes exist.
- Repositories must be publicly accessible, or authentication must be configured via git credentials or SSH keys.
- On systems with limited network bandwidth or CPU resources, consider reducing the parallelism level (the `-P` parameter) to avoid overwhelming the system.
