# pull-ai Documentation

## Overview

`pull-ai` is a Fish shell script that automates the parallel downloading of AI model variants using Ollama. It creates a tmux session with multiple panes to simultaneously download multiple model variants, optimising bandwidth utilisation and reducing total download time by leveraging multi-pane terminal multiplexing.

## Description

This utility streamlines the process of acquiring large language models by orchestrating concurrent downloads across separate tmux panes. Rather than downloading models sequentially (which would require waiting for one download to complete before starting the next), `pull-ai` initiates all downloads in parallel, significantly reducing the overall time required to obtain all desired models.

The script currently targets three model variants:

- `qwen2.5:72b` – The 72 billion parameter Qwen 2.5 model
- `qwen3:235b` – The 235 billion parameter Qwen 3 model
- `deepseek-r1:671b` – The 671 billion parameter DeepSeek-R1 model

## Usage

### Basic Invocation

```bash
./pull-ai.fish
```

Simply execute the script with no arguments. The script will:

1. Verify that required dependencies are installed
2. Terminate any pre-existing tmux session named `qwen_downloads`
3. Create a new tmux session with multiple panes
4. Initiate model downloads in each pane
5. Attach to the tmux session to display download progress

### Keyboard Shortcuts

While attached to the tmux session:

- **`Ctrl+B` followed by `D`** – Detach from the session without interrupting downloads
- **`Ctrl+B` followed by `C`** – Create a new window within the session
- **`Ctrl+B` followed by `←/→`** – Navigate between panes (arrow keys)

### Reattaching to Downloads

If you detach from the session, you can reattach at any time:

```bash
tmux attach-session -t qwen_downloads
```

## CLI Arguments and Flags

The current version of `pull-ai` does not accept command-line arguments or flags. The script uses a hardcoded list of three model variants. Future enhancements could add flexibility through optional parameters.

## Dependencies

The script requires the following software to be installed and accessible via the system PATH:

- **Fish shell** – The script interpreter (typically invoked as `fish` or via the shebang `#!/usr/bin/env fish`)
- **tmux** – Terminal multiplexer for creating and managing multiple panes
- **ollama** – AI model management tool responsible for downloading and executing models

If either tmux or ollama is unavailable, the script will exit with a descriptive error message.

## Installation

1. Ensure Fish shell, tmux, and ollama are installed on your system
2. Place `pull-ai.fish` in a directory on your PATH (e.g., `/usr/local/bin` or `~/bin`)
3. Make the script executable:
   ```bash
   chmod +x /path/to/pull-ai.fish
   ```

## Notable Implementation Details

### Dependency Validation

The script performs early validation of required tools using the Fish `command -v` builtin:

```fish
if not command -v tmux >/dev/null
    echo "Error: tmux is not installed. Please install tmux first."
    exit 1
end
```

This ensures meaningful error messages if dependencies are missing, rather than cryptic failures mid-execution.

### Session Management

The script kills any existing tmux session named `qwen_downloads` before creating a new one:

```fish
tmux kill-session -t qwen_downloads 2>/dev/null
```

This prevents conflicts with previously created sessions and allows the script to be run multiple times without manual cleanup.

### Dynamic Pane Layout

The script employs conditional logic to arrange panes in a sensible layout:

- **Panes 1–3**: Arranged horizontally (`even-horizontal` layout)
- **Panes 4–5**: Moved to the bottom half and arranged with tiling
- **Panes 6–7**: Arranged vertically on the right side

The final layout is set to `tiled` to automatically balance all panes on the screen, maximising readability of download progress from all panes simultaneously.

### Model List as Fish Array

Models are defined as a Fish array variable:

```fish
set models qwen2.5:72b qwen3:235b deepseek-r1:671b
```

This approach makes it straightforward to modify the list of models or extend the script for additional variants in future versions.

### Ollama Integration

Each pane executes an `ollama pull` command for its assigned model:

```fish
ollama pull $models[$i]
```

The script provides user feedback via echo statements in each pane, which display the model being downloaded before the pull operation begins.

### User Guidance

The script provides clear instructions for detaching and reattaching:

```
Attaching to tmux session. Press Ctrl+B then D to detach without stopping downloads.
If you've detached from the session, you can reattach with:
tmux attach-session -t qwen_downloads
```

This guidance helps users who may be unfamiliar with tmux understand how to manage the session without terminating downloads.

## Limitations and Future Enhancements

- **Fixed Model List** – Models are currently hardcoded; parameterisation via command-line arguments would improve flexibility
- **No Download Verification** – The script does not verify downloaded models or check available disk space beforehand
- **Sequential Pane Creation** – The loop creates panes sequentially, which could be optimised for cleaner pane creation
- **Error Handling** – Individual download failures within panes are not caught or reported to the user; monitoring requires manual inspection

## Examples

### Standard Usage

```bash
$ ./pull-ai.fish
Starting tmux session for parallel downloads...
Starting downloads for all Qwen2.5 model variants in parallel...
Attaching to tmux session. Press Ctrl+B then D to detach without stopping downloads.
[tmux session opens with three panes downloading models in parallel]
```

### Reattaching After Detachment

```bash
$ tmux attach-session -t qwen_downloads
[displays current download progress in all three panes]
```

## Troubleshooting

### tmux or ollama Not Found

**Problem**: The script exits immediately with "Error: tmux is not installed" or "Error: ollama is not installed"

**Solution**: Install the missing tool using your system's package manager:

- **Ubuntu/Debian**: `sudo apt-get install tmux` or `sudo apt-get install ollama`
- **macOS**: `brew install tmux` or `brew install ollama`
- **Fedora/RHEL**: `sudo dnf install tmux` or `sudo dnf install ollama`

### Session Already Exists

**Problem**: The script appears to freeze or display unexpected behaviour

**Solution**: The script automatically kills the previous session, but if issues persist, manually kill it:

```bash
tmux kill-session -t qwen_downloads
```

### Downloads Not Starting

**Problem**: Panes appear empty or do not display download progress

**Solution**: Verify that ollama is running:

```bash
ollama serve
```

In a separate terminal, attempt a manual download to diagnose issues:

```bash
ollama pull qwen2.5:72b
```
