# Cloudflare Pages Deployment Cleanup Utility

## Overview

`delete-workers-deployments.js` is a utility script that automatically removes old deployments from a Cloudflare Pages project whilst preserving the current production deployment. This tool helps manage and clean up accumulated deployments to reduce clutter and potentially improve project management within Cloudflare Pages.

## Description

The utility leverages the Cloudflare API to:

- Identify the current production deployment (canonical deployment) in a specified Pages project
- Retrieve a complete list of all deployments, handling pagination automatically
- Filter out the production deployment to ensure it is never deleted
- Delete all non-production deployments with retry logic and rate limiting
- Provide detailed feedback on deletion success and failures

This is particularly useful for projects that deploy frequently and accumulate many historical deployments over time.

## Prerequisites

### Runtime Environment

- **Bun** (v1.0 or later) – The script is designed to run with the Bun JavaScript runtime

### Dependencies

- No external npm packages required (uses native Bun APIs)

### Cloudflare Configuration

- Active Cloudflare account with API access
- Cloudflare Pages project set up
- Valid Cloudflare API credentials (API Key and account email)
- Account ID and Pages project name

## Configuration

Before running the script, you must edit the configuration section at the top of the file and populate the following variables:

```javascript
const CF_API_KEY = ""; // Your Cloudflare Global API Key
const CF_EMAIL = ""; // Email associated with your Cloudflare account
const CF_ACCOUNT_ID = ""; // Your Cloudflare account ID
const CF_PAGES_PROJECT_NAME = ""; // Name of the Pages project to clean up
const CF_DELETE_ALIASED_DEPLOYMENTS = true; // Force delete aliased deployments
```

### Configuration Details

- **CF_API_KEY**: Your Cloudflare Global API Key (not a scoped token). Obtain this from your Cloudflare account settings under API Tokens.
- **CF_EMAIL**: The email address associated with your Cloudflare account.
- **CF_ACCOUNT_ID**: Your Cloudflare account ID, visible in the dashboard URL or account settings.
- **CF_PAGES_PROJECT_NAME**: The exact name of your Cloudflare Pages project.
- **CF_DELETE_ALIASED_DEPLOYMENTS**: Set to `true` to force deletion of deployments with aliases; set to `false` to skip them.

Optional tuning parameters:

```javascript
const MAX_RETRIES = 3; // Number of retries for failed deletions
const DELAY_BETWEEN_REQUESTS = 500; // Milliseconds to wait between API requests
```

## Usage

### Basic Execution

```bash
bun /path/to/delete-workers-deployments.js
```

Or, if the file has execute permissions:

```bash
./delete-workers-deployments.js
```

### Command-Line Arguments

Currently, this utility does **not** accept command-line arguments or flags. All configuration must be done by editing the script directly.

### Example Output

```
🚀 Starting Cloudflare Pages deployment cleanup...

🔍 Fetching production deployment info...
✅ Production deployment: abc123def456
📋 Fetching all deployments...
   Fetching page 1...
📊 Found 47 total deployments

🎯 Will delete 46 deployments (keeping production: abc123def456)

🗑️  Deleted: old-deploy-001 (production, 2024-01-15T10:30:00Z)
🗑️  Deleted: old-deploy-002 (preview, 2024-01-14T09:15:00Z)
...

✅ Cleanup complete!
   Deleted: 46
   Failed: 0
   Kept (production): 1
```

## Notable Implementation Details

### Production Deployment Preservation

The script automatically identifies the production deployment by querying the project's canonical deployment. This deployment is explicitly excluded from deletion, ensuring the active production environment is never removed.

### Pagination Handling

The utility fetches deployments in pages of 25 (Cloudflare's default) and automatically continues through all available pages. A 100ms delay is inserted between page requests to avoid overwhelming the API.

### Retry Logic with Exponential Backoff

Failed deletion requests are automatically retried up to 3 times (configurable via `MAX_RETRIES`). Each retry uses exponential backoff: retry 1 waits 1 second, retry 2 waits 2 seconds, and retry 3 waits 3 seconds.

### Rate Limiting

A configurable delay (`DELAY_BETWEEN_REQUESTS`, default 500ms) is applied between deletion requests to respect Cloudflare's rate limits and avoid throttling.

### Forced Deletion Mode

When `CF_DELETE_ALIASED_DEPLOYMENTS` is set to `true`, the script appends `?force=true` to deletion requests, allowing deletion of deployments that have aliases assigned. Set to `false` to skip deployments with aliases.

### Error Handling

- Configuration validation ensures all required fields are populated before API calls begin
- HTTP errors are caught and reported with status codes and messages
- API error responses are logged in detail (JSON format)
- Failed deletions are tracked separately and reported in the final summary
- The script exits with status code 1 on critical errors

### API Authentication

The script uses Cloudflare's X-Auth-Key and X-Auth-Email headers for authentication. These are sent with every API request.

## Error Handling and Troubleshooting

### Configuration Errors

**Error**: `CF_API_KEY is required`

- **Solution**: Ensure you have populated the `CF_API_KEY` variable at the top of the script.

**Error**: `CF_EMAIL is required` / `CF_ACCOUNT_ID is required` / `CF_PAGES_PROJECT_NAME is required`

- **Solution**: Populate all four configuration variables before running the script.

### API Errors

**Error**: `HTTP 401: Unauthorized`

- **Solution**: Check that your API key and email are correct and have the necessary permissions.

**Error**: `HTTP 404: Not Found`

- **Solution**: Verify the account ID and project name are correct. The project name is case-sensitive.

**Error**: `No production deployment found`

- **Solution**: Ensure your Pages project has at least one production deployment.

### Deletion Failures

If a deployment fails to delete after all retries, it will be logged with an error message. The script continues processing remaining deployments and reports the count of failures at the end.

## Security Considerations

- **API Key Management**: Store your API key securely. Do not commit the configured script to version control with credentials populated.
- **Credential Exposure**: The script does not accept credentials as command-line arguments to avoid exposure in process listings or shell history.
- **Token Scope**: Use a Cloudflare API token with minimal required permissions (Cloudflare Pages read/delete) rather than a global API key if your account supports it.

## Limitations

- **No CLI Arguments**: Configuration must be edited directly in the file; command-line arguments are not supported.
- **Single Project**: The script targets one project at a time. Running against multiple projects requires separate executions.
- **Synchronous Execution**: Deployments are deleted sequentially (with delays), not in parallel. Large numbers of deployments may take considerable time to process.

## Related Resources

- [Cloudflare Pages API Documentation](https://developers.cloudflare.com/api/operations/pages-project-list)
- [Cloudflare API Authentication](https://developers.cloudflare.com/api/tokens/create)
- [Bun Documentation](https://bun.sh)
