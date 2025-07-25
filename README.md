# YouTube Subscriptions Manager

A command-line tool to manage YouTube subscriptions - export your subscriptions to CSV and batch unsubscribe from channels.

## Features

- **Export subscriptions**: Download all your YouTube subscriptions to a CSV file with comprehensive metadata
- **Batch unsubscribe**: Mark channels in the CSV and unsubscribe from multiple channels at once
- **Rich data export**: Includes channel IDs, subscription dates, video counts, thumbnails, and more
- **Robust error handling**: Automatic retries, rate limit handling, and detailed error messages
- **Progress tracking**: Visual progress bars and status updates during operations

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google Cloud project with YouTube Data API v3 enabled

### Setup

1. Clone the repository:

```bash
git clone https://github.com/daveio/myriad.git
cd myriad
```

2. Install dependencies:

```bash
uv sync
```

3. Set up YouTube API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3:
     - Navigate to "APIs & Services" > "Library"
     - Search for "YouTube Data API v3"
     - Click "Enable"
   - Create OAuth2 credentials:
     - Go to "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "OAuth client ID"
     - Choose "Desktop application" as the application type
     - Download the credentials JSON file
   - Save the file as `client_secrets.json` in the project root

## Usage

### List Subscriptions

Export all your YouTube subscriptions to a CSV file:

```bash
# Export to auto-generated timestamped file
uv run subscriptions list

# Export to specific file
uv run subscriptions list my_subscriptions.csv

# Filter for channels inactive since a specific date
uv run subscriptions list --filter-date 2024-01-01
```

The CSV file includes:

- Channel name and ID
- Channel description
- Subscription ID and date
- Channel thumbnail URL
- Total video count
- Unwatched video count
- Last video date (when the channel last posted)
- Unsubscribe column (for marking channels)

### Unsubscribe from Channels

1. First, export your subscriptions:

```bash
uv run subscriptions list subscriptions.csv
```

2. Open the CSV file and add any value (e.g., "x", "yes", "1") to the `unsubscribe` column for channels you want to remove

3. Run the unsubscribe command:

```bash
uv run subscriptions unsubscribe subscriptions.csv
```

The tool will:

- Show progress for each unsubscription
- Continue processing even if some fail
- Provide a summary of successful/failed operations
- Include automatic retry logic for transient errors

## CSV Format

| Column          | Description                                         |
| --------------- | --------------------------------------------------- |
| channel_name    | Display name of the YouTube channel                 |
| channel_id      | Unique ID of the subscribed channel                 |
| description     | Channel description (cleaned for CSV compatibility) |
| subscription_id | Internal ID used for unsubscription                 |
| published_at    | When you subscribed (ISO format)                    |
| thumbnail_url   | Channel's profile image URL                         |
| video_count     | Total videos in channel                             |
| new_video_count | Number of unwatched videos                          |
| last_video_date | Date of the channel's most recent video             |
| unsubscribe     | Mark with any value to unsubscribe                  |

## Authentication

On first run, the tool will:

1. Open your default browser for Google OAuth2 authentication
2. Ask you to authorize access to your YouTube account
3. Save credentials to `token.json` for future use

The tool only requests the minimum required scope: `https://www.googleapis.com/auth/youtube`

## Error Handling

The tool handles various error scenarios:

- **API quota exceeded**: Gracefully reports and suggests waiting
  - YouTube API quotas reset daily at midnight Pacific Time (PT)
  - Default quota is 10,000 units per day
  - By default, saves partial results if quota is exceeded during filtering
  - Use `--no-save-partial` flag to disable saving partial results
- **Rate limits**: Automatic exponential backoff with retry
- **Network errors**: Detailed messages with troubleshooting steps
- **Invalid CSV format**: Validation before processing with helpful error messages

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Run tests (when available)
uv run pytest
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines]
