# MCP Tools Lister

## Overview

The MCP Tools Lister is a command-line utility that discovers and enumerates all available tools provided by Model Context Protocol (MCP) servers configured in Claude's configuration file. It connects to each MCP server sequentially, queries the available tools, and outputs a formatted list of tool identifiers for integration with Claude.

## Description

This utility serves as a tool discovery and inventory mechanism for MCP-based workflows. It reads the Claude configuration from the user's home directory, locates all registered MCP servers, establishes connections to each server, and retrieves the list of available tools. The output format is designed to be machine-readable, with each tool represented as `mcp__{serverName}__{toolName}`.

The utility is particularly useful for:

- Auditing which tools are available across all configured MCP servers
- Generating comprehensive tool lists for documentation or integration purposes
- Verifying that MCP servers are properly configured and accessible
- Debugging connectivity issues with specific MCP servers

## Installation Requirements

### Dependencies

- **Node.js Runtime**: Bun (https://bun.sh/)
- **npm Packages**:
  - `@modelcontextprotocol/sdk` – The official MCP SDK for client-server communication

### System Requirements

- Access to `~/.claude.json` configuration file
- Permissions to execute MCP server commands defined in the configuration
- Network/IPC access to all configured MCP servers

## Usage

### Basic Usage

```bash
./mcp-tools.ts
```

### Execution Method

This script is designed to be executed with Bun:

```bash
bun run mcp-tools.ts
```

Alternatively, if the script has execute permissions:

```bash
./mcp-tools.ts
```

### Output Format

The utility outputs tool identifiers to standard output, one per line:

```
mcp__serverName1__toolName1
mcp__serverName2__toolName2
mcp__serverName1__toolName3
```

Diagnostic and error messages are written to standard error (stderr), allowing for clean separation of results from logging information.

## CLI Arguments and Flags

The current implementation does not accept any command-line arguments or flags. The utility operates entirely based on the configuration defined in `~/.claude.json`.

## Configuration

### Configuration File Location

The utility reads from: `~/.claude.json` (user's home directory)

### Configuration Structure

The expected configuration format is:

```json
{
  "projects": {
    "/path/to/project": {
      "mcpServers": {
        "serverName": {
          "command": "path/to/server/executable",
          "args": ["arg1", "arg2"],
          "env": {
            "ENV_VAR": "value"
          }
        }
      }
    }
  }
}
```

### Configuration Parameters

- **projects**: Object mapping project paths to their configurations
- **mcpServers**: Object mapping server names to their connection details
  - **command**: The executable path or command to launch the MCP server
  - **args**: Array of command-line arguments passed to the server
  - **env** (optional): Object of environment variables to pass to the server process

## Notable Implementation Details

### Sequential Server Querying

The utility queries MCP servers sequentially (one at a time) rather than in parallel. This approach:

- Prevents resource exhaustion on the host system
- Allows graceful handling of individual server failures
- Provides readable, ordered diagnostic output

### Tavily Server Exclusion

The utility explicitly skips the "tavily" MCP server by default due to known connection issues. This is a hard-coded exclusion to prevent unnecessary errors during tool discovery.

### Error Handling

- Individual server failures do not halt the entire process; the utility continues querying remaining servers
- Connection errors are logged to stderr but do not prevent the output of successfully discovered tools
- Proper resource cleanup is ensured through try-catch blocks when closing client connections

### Transport Mechanism

The utility uses `StdioClientTransport` from the MCP SDK, meaning MCP servers communicate via standard input/output (stdin/stdout) rather than network sockets.

### Environment Variable Inheritance

The script preserves the current process environment and merges it with any server-specific environment variables defined in the configuration. Server-specific variables take precedence over inherited ones.

### Configuration Discovery Logic

When multiple projects are defined in the configuration file, the utility uses the first project that has MCP servers configured. If no projects contain MCP servers, the utility exits with an error.

## Error Handling

The utility handles various error conditions:

| Error Scenario                               | Behaviour                                                       |
| -------------------------------------------- | --------------------------------------------------------------- |
| Configuration file not found or invalid JSON | Exit with status code 1; error message printed to stderr        |
| No MCP servers configured                    | Exit with status code 1; "No MCP servers found" message printed |
| Individual server connection failure         | Log error to stderr; continue processing remaining servers      |
| Fatal runtime error                          | Exit with status code 1; error message printed to stderr        |

## Example Output

Given a configuration with three MCP servers (claude-code, github, and slack) with varying numbers of tools:

```
mcp__claude-code__readFile
mcp__claude-code__writeFile
mcp__claude-code__executeCommand
mcp__github__createIssue
mcp__github__listIssues
mcp__slack__sendMessage
```

Standard error output during execution:

```
Reading Claude configuration...
Found 3 MCP servers
Querying claude-code...
  Found 3 tools
Querying github...
  Found 2 tools
Skipping tavily (known to have connection issues)
Querying slack...
  Found 1 tools

Total tools found: 6
```

## Troubleshooting

### "No MCP servers found in Claude configuration"

**Cause**: No projects in `~/.claude.json` have the `mcpServers` field configured.

**Solution**: Verify that `~/.claude.json` contains at least one project with MCP servers defined.

### "Failed to query [serverName]"

**Cause**: The utility could not establish a connection to the specified MCP server or the server did not respond with a valid tool list.

**Solution**:

- Verify the server executable path is correct
- Ensure the server process can be launched
- Check that any required environment variables are set

### Missing output for specific servers

**Cause**: The server may have been skipped (e.g., tavily) or encountered an error during connection.

**Solution**: Check stderr output for diagnostic messages regarding the specific server.

## Notes for Users

- The utility connects to and disconnects from each MCP server independently, so running it multiple times is safe and does not require special cleanup.
- Tool enumeration may be slow if many MCP servers are configured or if servers have slow startup times.
- Some MCP servers may not implement the `listTools` method; in such cases, an error will be logged and that server will be skipped.
