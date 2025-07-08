# Gmail Unsubscribe Tool

A powerful CLI tool for automating email unsubscribe processes using the Gmail API. This tool scans your Gmail for emails with `List-Unsubscribe` headers and allows you to efficiently process unsubscribe requests.

## Features

- 🔍 **Smart Scanning**: Scan specific Gmail labels for emails with unsubscribe information
- 📊 **CSV Export**: Generate timestamped CSV files with detailed unsubscribe data
- 🔄 **Resume Support**: Continue interrupted scans or processing sessions
- 📧 **Email Unsubscribe**: Send automated unsubscribe emails via Gmail API
- 🌐 **HTTP Unsubscribe**: Make HTTP requests to unsubscribe links
- 🖱️ **Browser Mode**: Open unsubscribe links in your default browser
- 🎨 **Rich UI**: Beautiful progress bars and colored terminal output
- 🔐 **Secure**: Uses official Google OAuth2 authentication

## Installation

This tool requires Python 3.8+ and uses `uv` for dependency management.

```bash
# Clone or navigate to the project directory
cd /path/to/unsubscribe

# Install dependencies with uv
uv sync

# Or install with pip
pip install -e .
```

## Setup

### 1. Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID) for a desktop application
5. Download the credentials JSON file

### 2. Environment Configuration

You can provide your API credentials in two ways:

**Option A: Command line parameter**

```bash
unsubscribe --api-key /path/to/credentials.json scan
```

**Option B: Environment variable**

```bash
export GMAIL_API_KEY=/path/to/credentials.json
unsubscribe scan
```

## Usage

### Scanning for Unsubscribe Information

#### Basic Scan (Inbox only)

```bash
unsubscribe scan
```

#### Scan Specific Labels

```bash
# Single label
unsubscribe scan --labels "Promotions"

# Multiple labels
unsubscribe scan --labels "Promotions,Updates,Marketing"
```

#### Resume a Previous Scan

```bash
unsubscribe scan --resume emails_2025_01_06_123456.csv
```

### Processing Unsubscribe Actions

After scanning, you'll get a CSV file with unsubscribe information. Edit the `action` column to specify what you want to do:

- `email` - Send unsubscribe email
- `http` - Make HTTP request to unsubscribe URL
- `both` - Try both email and HTTP methods
- Leave blank to skip

#### Process Unsubscribe Actions

```bash
unsubscribe run emails_2025_01_06_123456.csv
```

#### Use Browser Mode for HTTP Links

```bash
unsubscribe run emails_2025_01_06_123456.csv --http-browser
```

#### Resume Processing

```bash
unsubscribe run emails_2025_01_06_123456.csv --resume
```

## CSV File Format

The generated CSV files contain the following columns:

| Column              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| `from_address`      | Email address of the sender                            |
| `sender_name`       | Display name of the sender                             |
| `email_id`          | Gmail message ID                                       |
| `email_date`        | Email date in UNIX timestamp (for sorting)             |
| `unsubscribe_link`  | HTTP unsubscribe URL (if available)                    |
| `unsubscribe_email` | Email address for unsubscribe (if available)           |
| `action`            | Your chosen action (`email`, `http`, `both`, or blank) |
| `processed`         | Processing status (`True`, `Failed`, or blank)         |

## Example Workflow

1. **Scan your Promotions folder:**

   ```bash
   unsubscribe scan --labels "Promotions"
   ```

2. **Review the generated CSV file** (e.g., `emails_2025_01_06_123456.csv`)

3. **Edit the `action` column** to specify what you want to do for each sender:
   - Set to `email` for senders where you want to send an unsubscribe email
   - Set to `http` for senders where you want to click the unsubscribe link
   - Set to `both` to try both methods
   - Leave blank to skip

4. **Process the unsubscribe actions:**

   ```bash
   unsubscribe run emails_2025_01_06_123456.csv
   ```

5. **Check the results** in the updated CSV file

## Advanced Features

### Label Support

The tool supports Gmail's label system. You can scan:

- Built-in labels: `INBOX`, `SENT`, `DRAFT`, `SPAM`, `TRASH`
- Custom labels: `"My Custom Label"`, `"Work Email"`, etc.
- Multiple labels: `"Promotions,Updates,Social"`

### Resume Functionality

Both scanning and processing support resume functionality:

- **Scan Resume**: Continues from where a previous scan left off, avoiding duplicate work
- **Process Resume**: Skips entries that are already marked as processed

### HTTP vs Browser Mode

**HTTP Mode** (default):

- Makes automated HTTP requests to unsubscribe links
- Faster and more efficient
- May not work with complex unsubscribe forms

**Browser Mode** (`--http-browser`):

- Opens links in your default browser
- Allows manual interaction with complex forms
- Requires manual confirmation of each unsubscribe

## Safety Features

- **Confirmation prompts** before processing actions
- **Rate limiting** to avoid hitting API limits
- **Error handling** with detailed logging
- **Resume capability** if processing is interrupted
- **Timestamped files** to prevent accidental overwrites

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. Make sure the Gmail API is enabled in Google Cloud Console
2. Verify your credentials file is valid JSON
3. Check that your OAuth consent screen is configured
4. Delete `token.pickle` file to force re-authentication

### Rate Limiting

Gmail API has rate limits. If you hit them:

1. Wait a few minutes and try again
2. Use the resume functionality to continue where you left off
3. Consider processing smaller batches

### Missing Unsubscribe Information

Not all emails have `List-Unsubscribe` headers. This is normal and depends on the sender's email practices.

## Privacy and Security

- **Local Processing**: All data processing happens locally on your machine
- **OAuth2 Security**: Uses Google's secure OAuth2 flow
- **No Data Collection**: The tool doesn't send your data anywhere except to perform unsubscribe actions
- **Token Storage**: OAuth tokens are stored locally in `token.pickle`

## Development

### Running Tests

```bash
# Install development dependencies
uv sync --group dev

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Sort imports
isort src/

# Type checking
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Myriad monorepo and follows its licensing terms.

## Support

For issues, questions, or contributions, please use the GitHub issues system in the main Myriad repository.
