# Design Document

## Overview

This design outlines the implementation of a YouTube subscriptions management CLI tool built with Python, Click, and the Google API Python Client. The tool provides two main commands: `list` for downloading subscription data to CSV, and `unsubscribe` for batch unsubscribing from channels marked in the CSV file.

The tool leverages the YouTube Data API v3 for accessing subscription data and performing unsubscribe operations. Authentication is handled through OAuth2 flow using the Google API Python Client library.

## Architecture

The application follows a modular CLI architecture with the following components:

```
src/subscriptions/
├── __init__.py
├── cli.py              # Main CLI entry point with Click commands
├── auth.py             # OAuth2 authentication handling
├── youtube_client.py   # YouTube API client wrapper
├── csv_handler.py      # CSV file operations
└── utils.py            # Utility functions (date formatting, etc.)
```

The tool uses a layered architecture:

- **CLI Layer**: Click-based command interface
- **Service Layer**: YouTube API operations and CSV handling
- **Authentication Layer**: OAuth2 credential management
- **Data Layer**: CSV file I/O operations

## Components and Interfaces

### CLI Interface (cli.py)

The main CLI module uses Click to define two commands:

```python
@click.group()
def subscriptions():
    """YouTube subscriptions management tool."""
    pass

@subscriptions.command()
@click.argument('filename', required=False)
def list(filename):
    """Download subscriptions to CSV file."""
    pass

@subscriptions.command()
@click.argument('filename', required=True)
def unsubscribe(filename):
    """Unsubscribe from channels marked in CSV."""
    pass
```

### Authentication Module (auth.py)

Handles OAuth2 authentication flow using the Google API Python Client:

```python
class YouTubeAuthenticator:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.scopes = ['https://www.googleapis.com/auth/youtube']

    def get_authenticated_service(self):
        """Returns authenticated YouTube service object."""
        pass

    def _load_credentials(self):
        """Load existing credentials from token file."""
        pass

    def _save_credentials(self, credentials):
        """Save credentials to token file."""
        pass

    def _run_oauth_flow(self):
        """Run OAuth2 flow for new credentials."""
        pass
```

### YouTube Client (youtube_client.py)

Wraps YouTube API operations:

```python
class YouTubeClient:
    def __init__(self, service):
        self.service = service

    def get_subscriptions(self):
        """Fetch all user subscriptions with pagination."""
        pass

    def unsubscribe_from_channel(self, subscription_id):
        """Unsubscribe from a channel by subscription ID."""
        pass

    def _paginate_subscriptions(self, page_token=None):
        """Handle pagination for subscription listing."""
        pass
```

### CSV Handler (csv_handler.py)

Manages CSV file operations:

```python
class SubscriptionCSVHandler:
    def __init__(self, filename):
        self.filename = filename
        self.fieldnames = ['channel_name', 'description', 'subscription_id', 'unsubscribe']

    def write_subscriptions(self, subscriptions):
        """Write subscriptions data to CSV file."""
        pass

    def read_unsubscribe_list(self):
        """Read CSV and return channels marked for unsubscription."""
        pass

    def _format_subscription_row(self, subscription):
        """Format subscription data for CSV row."""
        pass
```

### Utilities (utils.py)

Helper functions:

```python
def generate_default_filename():
    """Generate default filename with timestamp."""
    pass

def validate_csv_format(filename):
    """Validate CSV file has required columns."""
    pass
```

## Data Models

### Subscription Data Structure

Based on YouTube API v3 subscription resource:

```python
{
    'id': 'subscription_id',
    'snippet': {
        'title': 'Channel Name',
        'description': 'Channel Description',
        'resourceId': {
            'channelId': 'channel_id'
        }
    }
}
```

### CSV File Format

```csv
channel_name,description,subscription_id,unsubscribe
"Example Channel","Channel description here","UCxxxxxxxxxxxxxxxxxxxxx",""
"Another Channel","Another description","UCyyyyyyyyyyyyyyyyyyyyyy","yes"
```

## Error Handling

### Authentication Errors

- Missing credentials file: Provide clear instructions for obtaining credentials
- Expired tokens: Automatically refresh or prompt for re-authentication
- Invalid scopes: Guide user to correct OAuth2 setup

### API Errors

- Rate limiting: Implement exponential backoff and retry logic
- Network errors: Retry with timeout and provide meaningful error messages
- Invalid subscription IDs: Log errors but continue processing other subscriptions

### File Operations

- Missing CSV file: Clear error message with file path
- Invalid CSV format: Validate headers and provide format guidance
- Permission errors: Check file permissions and provide solutions

### Error Handling Strategy

```python
class YouTubeSubscriptionsError(Exception):
    """Base exception for YouTube subscriptions tool."""
    pass

class AuthenticationError(YouTubeSubscriptionsError):
    """Authentication-related errors."""
    pass

class APIError(YouTubeSubscriptionsError):
    """YouTube API-related errors."""
    pass

class FileError(YouTubeSubscriptionsError):
    """File operation errors."""
    pass
```

## Testing Strategy

### Unit Tests

- Test each module independently with mocked dependencies
- Test CSV parsing and generation logic
- Test authentication flow with mock credentials
- Test error handling scenarios

### Integration Tests

- Test complete workflow with test YouTube account
- Test OAuth2 flow end-to-end
- Test CSV file operations with temporary files
- Test API rate limiting and error recovery

### Test Structure

```
tests/
├── unit/
│   ├── test_auth.py
│   ├── test_youtube_client.py
│   ├── test_csv_handler.py
│   └── test_utils.py
├── integration/
│   ├── test_list_command.py
│   ├── test_unsubscribe_command.py
│   └── test_oauth_flow.py
└── fixtures/
    ├── sample_subscriptions.json
    └── sample_subscriptions.csv
```

### Dependencies and Package Management

The tool will use the following key dependencies:

- `click`: CLI framework for command-line interface
- `google-api-python-client`: Official Google API client
- `google-auth-oauthlib`: OAuth2 authentication flow
- `google-auth-httplib2`: HTTP transport for Google Auth

Package management via `uv` with dependencies declared in `pyproject.toml`:

```toml
[project]
name = "subscriptions"
dependencies = [
    "click>=8.0.0",
    "google-api-python-client>=2.0.0",
    "google-auth-oauthlib>=1.0.0",
    "google-auth-httplib2>=0.2.0",
]

[project.scripts]
subscriptions = "subscriptions.cli:subscriptions"
```

## Security Considerations

- Store OAuth2 credentials securely in user's home directory
- Never log or expose API keys or tokens
- Validate all user inputs to prevent injection attacks
- Use HTTPS for all API communications
- Implement proper file permissions for credential storage

## Performance Considerations

- Implement pagination for large subscription lists
- Use batch operations where possible
- Implement rate limiting to respect YouTube API quotas
- Cache authentication tokens to avoid repeated OAuth flows
- Process unsubscriptions with appropriate delays to avoid rate limits
