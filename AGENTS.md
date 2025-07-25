# YouTube Subscriptions Tool

A Python CLI tool for managing YouTube subscriptions - list all subscriptions to CSV and batch unsubscribe from channels.

## Architecture Overview

The tool is structured as a Python package with the following components:

- **CLI Module** (`cli.py`): Entry point using Click framework, handles user commands
- **Authentication** (`auth.py`): OAuth2 flow for YouTube API authentication
- **YouTube Client** (`youtube_client.py`): Wrapper for YouTube Data API v3 with retry logic
- **CSV Handler** (`csv_handler.py`): Manages reading/writing subscription data to CSV files
- **Utilities** (`utils.py`): Common exceptions, validators, and helper functions

## Key Features

- Fetches all YouTube subscription data including channel IDs, thumbnails, video counts, and subscription dates
- Exports subscriptions to CSV with comprehensive metadata
- Batch unsubscribe from channels marked in CSV
- Robust error handling with retry logic for API rate limits
- OAuth2 authentication flow with credential caching

## Development Commands

```bash
# Install dependencies with uv
uv sync

# Run the CLI tool
uv run subscriptions list                    # List all subscriptions to timestamped CSV
uv run subscriptions list output.csv         # List to specific file
uv run subscriptions unsubscribe marked.csv  # Unsubscribe from marked channels

# Development setup
uv sync --dev  # Install with dev dependencies
```

## API Integration

The tool uses YouTube Data API v3 with the following parts:

- `snippet`: Basic subscription info (title, description, thumbnails)
- `contentDetails`: Video counts and activity info
- `subscriberSnippet`: Additional subscriber channel details

## CSV Format

The tool exports/imports CSV files with these columns:

- `channel_name`: Display name of the YouTube channel
- `channel_id`: Unique ID of the subscribed channel
- `description`: Channel description (multi-line content is cleaned)
- `subscription_id`: Internal ID for unsubscription operations
- `published_at`: ISO timestamp of when subscription was created
- `thumbnail_url`: High-quality channel thumbnail URL
- `video_count`: Total videos in channel
- `new_video_count`: Number of unwatched videos
- `unsubscribe`: Mark with any value to unsubscribe

## Authentication Setup

1. Create a Google Cloud project and enable YouTube Data API v3
2. Create OAuth2 credentials (Desktop application type)
3. Download credentials as `client_secrets.json`
4. Place in project root directory
5. First run will open browser for authorization
6. Token is cached in `token.json` for subsequent runs

## Error Handling

The tool includes sophisticated error handling:

- Exponential backoff with jitter for rate limits
- Automatic retry for transient errors (5xx, 429)
- Detailed error messages with troubleshooting steps
- Graceful handling of quota exceeded errors
- Validation of CSV format before processing

## Recent Changes

- Fixed duplicate exception class definitions
- Added all available YouTube API data fields to CSV export
- Implemented proper multi-line description handling
- Enhanced error details extraction for better debugging
- Moved time import to module level
