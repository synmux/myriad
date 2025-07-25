"""Main CLI entry point for YouTube subscriptions management tool."""

import sys
import time

import click

from .auth import YouTubeAuthenticator
from .csv_handler import SubscriptionCSVHandler
from .utils import (
    APIError,
    AuthenticationError,
    FileError,
    format_error_message,
    generate_default_filename,
)
from .youtube_client import YouTubeClient


@click.group()
def subscriptions():
    """YouTube subscriptions management tool.

    This tool helps you manage your YouTube subscriptions by providing two main commands:

    • list: Download your current subscriptions to a CSV file
    • unsubscribe: Batch unsubscribe from channels marked in a CSV file

    Before using this tool, you'll need:
    1. A Google Cloud project with YouTube Data API v3 enabled
    2. OAuth2 credentials (credentials.json file)
    3. Internet connection for API access

    Examples:
        uv run subscriptions list
        uv run subscriptions list my_subs.csv
        uv run subscriptions unsubscribe my_subs.csv

    For detailed help on each command, use:
        uv run subscriptions COMMAND --help
    """
    pass


@subscriptions.command()
@click.argument("filename", required=False, metavar="[FILENAME]")
def list(filename):
    """Download your YouTube subscriptions to a CSV file.

    This command authenticates with YouTube using OAuth2, fetches all your current
    subscriptions, and saves them to a CSV file. The CSV file will contain columns
    for channel name, description, subscription ID, and an empty 'unsubscribe' field
    that you can fill out to mark channels for batch unsubscription.

    FILENAME is optional. If not provided, a timestamped filename will be generated
    automatically in the format: subscriptions-YYMMdd-HHmmss.csv

    The CSV format includes these columns:
    • channel_name: The display name of the YouTube channel
    • channel_id: The unique ID of the subscribed channel
    • description: Brief description of the channel
    • subscription_id: Internal ID used for unsubscription operations
    • published_at: When the subscription was created
    • thumbnail_url: URL of the channel's thumbnail image
    • video_count: Total number of videos in the channel
    • new_video_count: Number of unwatched videos
    • unsubscribe: Empty field you can fill to mark channels for removal

    Examples:
        # Download to auto-generated timestamped file
        uv run subscriptions list

        # Download to specific filename
        uv run subscriptions list my_subscriptions.csv

        # Download to file in specific directory
        uv run subscriptions list ~/Downloads/youtube_subs.csv

    Note: This command requires internet access and valid YouTube API credentials.
    On first run, you'll be prompted to complete OAuth2 authentication in your browser.
    """
    # Use default filename if none provided
    if not filename:
        filename = generate_default_filename()

    try:
        # Initialize components
        click.echo("🔐 Authenticating with YouTube...")
        authenticator = YouTubeAuthenticator()
        service = authenticator.get_authenticated_service()

        youtube_client = YouTubeClient(service)
        csv_handler = SubscriptionCSVHandler(filename)

        # Fetch subscriptions
        click.echo("📥 Downloading subscriptions...")
        try:
            with click.progressbar(length=1, label="Fetching data") as bar:
                subscriptions = youtube_client.get_subscriptions()
                bar.update(1)
        except Exception as e:
            # Provide more context for subscription fetching errors
            if "quota" in str(e).lower():
                click.echo(
                    "⚠️  API quota exceeded. This can happen if you've made many requests recently.",
                    err=True,
                )
                click.echo(
                    "💡 Try again later or check your quota limits in the Google Cloud Console.",
                    err=True,
                )
            elif "rate limit" in str(e).lower():
                click.echo(
                    "⚠️  Rate limit exceeded. Please wait a moment before trying again.",
                    err=True,
                )
            raise

        if not subscriptions:
            click.echo("⚠️  No subscriptions found.")
            return

        # Write to CSV
        click.echo(f"💾 Writing {len(subscriptions)} subscriptions to {filename}...")
        csv_handler.write_subscriptions(subscriptions)

        # Success message
        click.echo(
            f"✅ Successfully downloaded {len(subscriptions)} subscriptions to {filename}"
        )

    except AuthenticationError as e:
        click.echo(f"❌ Authentication failed: {e}", err=True)
        sys.exit(1)
    except APIError as e:
        click.echo(f"❌ YouTube API error: {e}", err=True)
        sys.exit(1)
    except FileError as e:
        click.echo(f"❌ File error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        error_msg = format_error_message(e, "downloading subscriptions")
        click.echo(f"❌ Unexpected error: {error_msg}", err=True)
        sys.exit(1)


@subscriptions.command()
@click.argument("filename", required=True, metavar="FILENAME")
def unsubscribe(filename):
    """Batch unsubscribe from YouTube channels marked in a CSV file.

    This command reads a CSV file (typically generated by the 'list' command) and
    unsubscribes from any channels that have a non-empty value in the 'unsubscribe'
    column. You can mark channels for unsubscription by putting any value (like 'yes',
    'x', or '1') in the unsubscribe column.

    FILENAME must be a valid CSV file with the required columns:
    • channel_name: Display name of the channel
    • channel_id: The unique ID of the subscribed channel
    • description: Channel description
    • subscription_id: Internal subscription ID (required for API calls)
    • published_at: When the subscription was created
    • thumbnail_url: URL of the channel's thumbnail image
    • video_count: Total number of videos in the channel
    • new_video_count: Number of unwatched videos
    • unsubscribe: Mark with any non-empty value to unsubscribe

    The command will:
    1. Validate the CSV file format and check that it exists
    2. Authenticate with YouTube using OAuth2
    3. Process each marked channel with progress indicators
    4. Provide detailed success/failure reporting
    5. Include automatic retry logic for transient errors

    Safety features:
    • Only processes channels explicitly marked for unsubscription
    • Includes rate limiting to respect YouTube API quotas
    • Continues processing even if individual unsubscriptions fail
    • Provides detailed error reporting and troubleshooting guidance

    Examples:
        # Unsubscribe from channels marked in a CSV file
        uv run subscriptions unsubscribe subscriptions.csv

        # Process a custom CSV file
        uv run subscriptions unsubscribe ~/Downloads/channels_to_remove.csv

        # Typical workflow:
        # 1. uv run subscriptions list my_subs.csv
        # 2. Edit my_subs.csv to mark unwanted channels
        # 3. uv run subscriptions unsubscribe my_subs.csv

    Warning: This command makes permanent changes to your YouTube subscriptions.
    Make sure you've backed up your subscription list before running this command.

    Note: Large unsubscription lists may take considerable time due to API rate limits.
    The command includes progress indicators and can be safely interrupted and resumed.
    """
    try:
        # Initialize CSV handler and validate file
        click.echo(f"📄 Reading CSV file: {filename}")
        csv_handler = SubscriptionCSVHandler(filename)

        if not csv_handler.file_exists():
            click.echo(f"❌ File not found: {filename}", err=True)
            sys.exit(1)

        # Read channels marked for unsubscription
        unsubscribe_list = csv_handler.read_unsubscribe_list()

        if not unsubscribe_list:
            click.echo("ℹ️  No channels marked for unsubscription in the CSV file.")
            return

        click.echo(
            f"📋 Found {len(unsubscribe_list)} channels marked for unsubscription"
        )

        # Initialize authentication and YouTube client
        click.echo("🔐 Authenticating with YouTube...")
        authenticator = YouTubeAuthenticator()
        service = authenticator.get_authenticated_service()
        youtube_client = YouTubeClient(service)

        # Process unsubscriptions with progress bar
        successful_unsubscriptions = 0
        failed_unsubscriptions = 0
        errors_encountered = []

        click.echo("🗑️  Processing unsubscriptions...")
        click.echo(
            "💡 This may take a while for large lists. Each request includes a small delay to respect rate limits."
        )

        with click.progressbar(
            unsubscribe_list, label="Unsubscribing", show_eta=True, show_percent=True
        ) as channels:
            for channel in channels:
                channel_name = channel["channel_name"]
                subscription_id = channel["subscription_id"]

                try:
                    success = youtube_client.unsubscribe_from_channel(subscription_id)
                    if success:
                        successful_unsubscriptions += 1
                        click.echo(f"  ✅ Unsubscribed from: {channel_name}")
                    else:
                        failed_unsubscriptions += 1
                        click.echo(f"  ⚠️  Failed to unsubscribe from: {channel_name}")

                except Exception as e:
                    failed_unsubscriptions += 1
                    error_msg = str(e)
                    errors_encountered.append((channel_name, error_msg))

                    # Provide context for common errors
                    if "quota" in error_msg.lower():
                        click.echo(
                            f"  ❌ Quota exceeded for {channel_name}. Consider trying again later."
                        )
                    elif "rate limit" in error_msg.lower():
                        click.echo(
                            f"  ❌ Rate limited for {channel_name}. Automatic retry failed."
                        )
                    elif "not found" in error_msg.lower():
                        click.echo(
                            f"  ❌ Subscription not found for {channel_name} (may already be unsubscribed)"
                        )
                    else:
                        click.echo(f"  ❌ Error unsubscribing from {channel_name}: {e}")

                # Small delay to avoid hitting rate limits
                time.sleep(0.2)

        # Summary
        total_processed = successful_unsubscriptions + failed_unsubscriptions
        click.echo("\n📊 Unsubscription Summary:")
        click.echo(f"  • Total processed: {total_processed}")
        click.echo(f"  • Successful: {successful_unsubscriptions}")
        click.echo(f"  • Failed: {failed_unsubscriptions}")

        if successful_unsubscriptions > 0:
            click.echo(
                f"✅ Successfully unsubscribed from {successful_unsubscriptions} channels"
            )

        if failed_unsubscriptions > 0:
            click.echo(f"⚠️  {failed_unsubscriptions} unsubscriptions failed")

            # Provide guidance for failures
            if errors_encountered:
                click.echo("\n🔍 Common failure reasons and solutions:")
                quota_errors = sum(
                    1 for _, error in errors_encountered if "quota" in error.lower()
                )
                rate_limit_errors = sum(
                    1
                    for _, error in errors_encountered
                    if "rate limit" in error.lower()
                )
                not_found_errors = sum(
                    1 for _, error in errors_encountered if "not found" in error.lower()
                )

                if quota_errors > 0:
                    click.echo(
                        f"  • {quota_errors} quota exceeded errors - Try again later or check your API quota"
                    )
                if rate_limit_errors > 0:
                    click.echo(
                        f"  • {rate_limit_errors} rate limit errors - The tool already includes delays and retries"
                    )
                if not_found_errors > 0:
                    click.echo(
                        f"  • {not_found_errors} subscription not found - These may already be unsubscribed"
                    )

                other_errors = (
                    failed_unsubscriptions
                    - quota_errors
                    - rate_limit_errors
                    - not_found_errors
                )
                if other_errors > 0:
                    click.echo(
                        f"  • {other_errors} other errors - Check your internet connection and API credentials"
                    )

    except AuthenticationError as e:
        click.echo(f"❌ Authentication failed: {e}", err=True)
        sys.exit(1)
    except APIError as e:
        click.echo(f"❌ YouTube API error: {e}", err=True)
        sys.exit(1)
    except FileError as e:
        click.echo(f"❌ File error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        error_msg = format_error_message(e, "processing unsubscriptions")
        click.echo(f"❌ Unexpected error: {error_msg}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    subscriptions()
