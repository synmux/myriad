# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

```bash
# Install dependencies
uv sync

# Run the CLI tool
uv run subscriptions list                    # List subscriptions to timestamped CSV
uv run subscriptions list output.csv         # List to specific file
uv run subscriptions list --filter-date 2024-01-01  # List channels inactive since date
uv run subscriptions unsubscribe marked.csv  # Unsubscribe from marked channels

# Install with dev dependencies
uv sync --dev
```

## Code Architecture

The YouTube Subscriptions tool is a Python CLI application using:

- **Click** for command-line interface
- **Google API Python Client** for YouTube Data API v3
- **OAuth2** for authentication

### Module Structure

- `cli.py`: Entry point with Click commands (`list` and `unsubscribe`)
- `auth.py`: OAuth2 authentication flow and credential management
- `youtube_client.py`: YouTube API wrapper with retry logic
- `csv_handler.py`: CSV file I/O for subscription data
- `utils.py`: Shared exceptions and utility functions

### Key Design Patterns

1. **Exception Hierarchy**: All exceptions inherit from `YouTubeSubscriptionsError`
2. **Retry Logic**: Exponential backoff with jitter for API rate limits
3. **CSV Validation**: Strict column validation before processing
4. **Error Context**: Detailed error messages with troubleshooting steps

### API Integration Details

The tool requests these YouTube API parts:

- `snippet`: Basic subscription info
- `contentDetails`: Video counts
- `subscriberSnippet`: Additional channel details

Rate limiting is handled with:

- 0.1s delay between pagination requests
- 0.2s delay between unsubscribe operations
- Automatic retry with exponential backoff for 429/5xx errors

### CSV Data Format

Required columns for unsubscribe operation:

- `channel_name`: For display
- `channel_id`: Subscribed channel ID
- `subscription_id`: Required for API delete call
- `unsubscribe`: Any non-empty value triggers unsubscription

Additional columns in export:

- `description`: Channel description (newlines replaced with spaces)
- `published_at`: ISO timestamp
- `thumbnail_url`: High-res channel image
- `video_count`: Total channel videos
- `new_video_count`: Unwatched videos
- `last_video_date`: Date of the channel's most recent video

### Authentication Flow

1. Looks for `client_secrets.json` (OAuth2 credentials)
2. Checks for cached token in `token.json`
3. Refreshes expired tokens automatically
4. Opens browser for initial authorization
5. Caches credentials for future use

### Error Handling Strategy

- **403 Quota Exceeded**: Clear message to wait
- **429 Rate Limit**: Automatic retry with backoff
- **404 Not Found**: Likely already unsubscribed
- **5xx Server Errors**: Retry up to 3 times
- **CSV Errors**: Detailed validation messages
