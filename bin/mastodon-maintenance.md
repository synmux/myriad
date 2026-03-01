# Mastodon Maintenance Utility

## Description

The `mastodon-maintenance.fish` script is a Fish shell maintenance utility designed to perform routine database and cache cleanup operations on a Mastodon instance. It executes a series of administrative tasks using the `tootctl` command-line tool to remove cached content, orphaned media files, outdated preview cards, and old statuses. This script is intended to be run periodically (typically via cron or a task scheduler) to maintain the health and performance of a Mastodon server.

## Usage

### Basic Execution

To run the maintenance script, execute it directly:

```bash
./mastodon-maintenance.fish
```

Alternatively, if you have the script in your PATH or are running it from the Mastodon installation directory:

```bash
mastodon-maintenance.fish
```

### Prerequisites

- **Fish Shell**: This script must be executed using the Fish shell (`fish`). The shebang line `#!/usr/bin/env fish` ensures it runs with the correct interpreter.
- **Mastodon Installation**: The script assumes it is executed from within a Mastodon installation directory, as it references relative paths like `bin/tootctl`.
- **Rails Environment**: The script sets `RAILS_ENV=production` for all operations, ensuring they target the production database.
- **Permissions**: The user executing this script must have sufficient permissions to access the Mastodon installation and its database.

## Dependencies

The script relies on the following components:

- **Fish Shell**: The shell interpreter required to execute this script.
- **tootctl**: The Mastodon command-line administration tool, included with Mastodon installations. This is the primary tool that performs all maintenance operations.
- **Ruby and Rails**: Required by `tootctl` to function correctly (part of the Mastodon installation).
- **Database Access**: Direct or indirect access to the Mastodon PostgreSQL database.

## Operations Performed

The script executes the following maintenance tasks in sequence:

### 1. Clear Cache

```
RAILS_ENV=production bin/tootctl cache clear
```

Clears the application cache, removing cached objects and temporary data to free up memory and ensure fresh data is loaded.

### 2. Remove Orphaned Media

```
RAILS_ENV=production bin/tootctl media remove-orphans
```

Identifies and removes orphaned media files—media entries in the database that no longer have associated posts or accounts. This recovers disk space used by unreferenced files.

### 3. Remove Aged Media (Basic)

```
RAILS_ENV=production bin/tootctl media remove --days=7 --verbose
```

Removes media files older than 7 days that have been removed from posts. The `--verbose` flag provides detailed output of the removal process.

### 4. Remove Aged Media (With Profile Pruning)

```
RAILS_ENV=production bin/tootctl media remove --days=7 --prune-profiles --include-follows --verbose
```

Removes media files older than 7 days and additionally:

- `--prune-profiles`: Removes cached profile headers and avatars from remote accounts.
- `--include-follows`: Includes follow-related media in the removal.

### 5. Remove Aged Media (With Headers)

```
RAILS_ENV=production bin/tootctl media remove --days=7 --remove-headers --include-follows --verbose
```

Removes media files older than 7 days and additionally:

- `--remove-headers`: Removes custom header images from user profiles.
- `--include-follows`: Includes follow-related media in the removal.

### 6. Remove Expired Preview Cards

```
RAILS_ENV=production bin/tootctl preview_cards remove --days=7
```

Removes preview cards (cached link previews) older than 7 days. These are generated automatically when users share links, and older ones can safely be regenerated on demand.

### 7. Remove Expired Statuses and Compress Database

```
RAILS_ENV=production bin/tootctl statuses remove --days=7 --clean-followed --compress-database
```

Removes statuses (posts) older than 7 days and performs database maintenance:

- `--clean-followed`: Cleans up follow-related data.
- `--compress-database`: Optimises and compresses the database, improving query performance. **Note**: This operation locks the database and may cause temporary unavailability during execution.

## CLI Arguments and Flags

This script does not accept any command-line arguments or flags directly. All operations are hard-coded with the following parameters:

- **`--days=7`**: The age threshold (in days) for removal. Media, preview cards, and statuses older than 7 days are eligible for removal.
- **`--verbose`**: Provides detailed output for media removal operations, useful for monitoring and debugging.
- **`--prune-profiles`**: Removes cached remote account profile data.
- **`--include-follows`**: Includes follow-related media in removal operations.
- **`--remove-headers`**: Removes custom header images from profiles.
- **`--clean-followed`**: Cleans up follow-related database entries.
- **`--compress-database`**: Optimises the database structure and recovers unused space.

To modify these parameters (such as changing the 7-day threshold), you must edit the script directly.

## Notable Implementation Details

### Environment Variable

All `tootctl` commands are executed with `RAILS_ENV=production`, ensuring operations target the production database and environment. This is essential for correct behaviour.

### Relative Paths

The script uses relative paths (`bin/tootctl`) rather than absolute paths. This means the script must be executed from the Mastodon installation root directory for the commands to function correctly.

### Database Locking

The final operation (`tootctl statuses remove ... --compress-database`) locks the database during execution. This operation may cause service interruptions or slowdowns. It is recommended to schedule this script during low-traffic periods or maintenance windows.

### No Error Handling

The script does not include error handling or conditional logic. If any command fails, subsequent commands will continue to execute. For production environments, consider wrapping this script in error handling logic.

### Sequential Execution

All operations execute sequentially. The entire maintenance process may take several minutes depending on the size of your Mastodon instance. Plan accordingly when scheduling automated runs.

### Recommended Schedule

This script is well-suited for daily or weekly execution via cron. A suggested cron entry for daily execution at 02:00 (during low-traffic hours):

```cron
0 2 * * * cd /path/to/mastodon && ./mastodon-maintenance.fish >> /var/log/mastodon-maintenance.log 2>&1
```

## Cautions

- **Downtime Risk**: The `--compress-database` flag locks the database. Schedule maintenance during periods when reduced availability is acceptable.
- **Data Loss**: While these operations are designed to be safe, they permanently remove data. Ensure you have database backups before running this script in production.
- **Resource Usage**: These operations can be resource-intensive, especially on large instances. Monitor system resources during execution.
- **Remote Media**: The profile pruning operations remove cached content from remote instances. This content will be re-downloaded if needed, consuming additional bandwidth.

## Example: Scheduling with Cron

Add the following line to your crontab (edit with `crontab -e`):

```cron
0 3 * * 0 cd /path/to/mastodon && ./mastodon-maintenance.fish >> /var/log/mastodon-maintenance.log 2>&1
```

This schedules the maintenance script to run every Sunday at 03:00 UTC, logging output to `/var/log/mastodon-maintenance.log`.

Alternatively, use `systemd` timers for more sophisticated scheduling:

```ini
[Unit]
Description=Mastodon Maintenance
After=network.target

[Timer]
OnWeekly=Sunday
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## Support and Modifications

To customise the maintenance operations, edit the script directly. Common modifications include:

- **Change the age threshold**: Modify the `--days=7` parameter to a different value.
- **Add logging**: Redirect output to a log file using `>> /path/to/logfile.log 2>&1`.
- **Skip specific operations**: Comment out lines (prefix with `#`) to disable specific cleanup tasks.
- **Add error handling**: Wrap commands with conditional logic to check exit codes.

For additional information on `tootctl` commands and options, consult the official Mastodon documentation or run `bin/tootctl --help` within your Mastodon installation.
