# Gmail Unsubscriber

Automate email unsubscription using Gmail API. This tool processes emails labeled with 'pending-unsubscribe' and automatically unsubscribes you using the List-Unsubscribe header.

## Features

- **Gmail API Integration**: Securely access your Gmail account
- **Multiple Unsubscribe Methods**:
  - Email-based unsubscribe (mailto: links)
  - HTTP-based unsubscribe (GET/POST requests)
  - One-click unsubscribe support (RFC 8058)
  - Browser fallback for complex unsubscribe flows
- **Label Management**: Automatically updates email labels after processing
- **Safety Features**:
  - Dry-run mode to preview actions
  - Progress tracking
  - Detailed logging
  - Rate limiting protection

## Installation

1. Clone this repository or download the files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API for your project
4. Go to "APIs & Services" > "Credentials"
5. Click "Create Credentials" > "OAuth client ID"
6. Choose "Desktop app" as the application type
7. Download the credentials and save as `credentials.json` in the script directory

### 2. Gmail Label Setup

1. In Gmail, create a label called `pending-unsubscribe`
2. Apply this label to any emails you want to unsubscribe from
3. The script will automatically create an `unsubscribed` label for processed emails

## Usage

### View setup instructions
```bash
python gmail_unsubscriber.py setup
```

### List emails pending unsubscription
```bash
python gmail_unsubscriber.py list
```

### Process emails (dry run)
```bash
python gmail_unsubscriber.py process --dry-run
```

### Process emails (actual unsubscribe)
```bash
python gmail_unsubscriber.py process
```

### Process with options
```bash
# Process only 5 emails
python gmail_unsubscriber.py process --limit 5

# Don't open browser for complex unsubscribes
python gmail_unsubscriber.py process --no-browser

# Custom delay between requests (in seconds)
python gmail_unsubscriber.py process --delay 5
```

## How it Works

1. **Label Detection**: Finds all emails with the `pending-unsubscribe` label
2. **Header Extraction**: Extracts the `List-Unsubscribe` header from each email
3. **Unsubscribe Methods**:
   - Tries HTTP unsubscribe first (preferred method)
   - Falls back to email-based unsubscribe if HTTP fails
   - Opens browser for manual intervention when needed
4. **Label Update**: Removes `pending-unsubscribe` and adds `unsubscribed` label

## Supported Unsubscribe Methods

- **One-Click Unsubscribe**: RFC 8058 compliant POST requests
- **HTTP GET**: Standard unsubscribe links
- **Email**: Sends unsubscribe email to specified address
- **Browser Fallback**: Opens complex unsubscribe pages in browser

## Security Notes

- Credentials are stored locally in `token.pickle`
- Only requests Gmail modify scope (not full access)
- No data is sent to third parties
- All unsubscribe requests go directly to the sender's systems

## Troubleshooting

### "Credentials file not found"
- Make sure you've downloaded `credentials.json` from Google Cloud Console
- Place it in the same directory as the script

### "Label not found"
- Create the `pending-unsubscribe` label in Gmail
- Label names are case-insensitive

### Rate limiting
- Increase the delay between requests using `--delay`
- Process fewer emails at once using `--limit`

## Limitations

- Some emails may not have List-Unsubscribe headers
- Complex unsubscribe flows may require manual browser interaction
- Rate limits apply to both Gmail API and HTTP requests

## License

MIT License - feel free to modify and distribute