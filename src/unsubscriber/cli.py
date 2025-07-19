"""
Enhanced CLI with pretty output and threading support
"""

import structlog
import click
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from .auth import GmailAuthenticator
from .gmail_service import GmailService
from .processors import EmailProcessor
from .unsubscribe import UnsubscribeHandler
from .utils import extract_headers
from .config import (
    DEFAULT_THREAD_COUNT, DEFAULT_DELAY_SECONDS,
    DEFAULT_MAX_RESULTS, LABEL_PENDING, console, configure_logging
)

logger = structlog.get_logger()


@click.group()
@click.option('--credentials', default='credentials.json', 
              help='Path to Gmail API credentials file')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose logging output')
@click.pass_context
def cli(ctx, credentials, verbose):
    """Gmail Unsubscriber - Automate email unsubscription with style 🚀"""
    ctx.ensure_object(dict)
    
    # Configure logging based on verbosity
    configure_logging(verbose)
    ctx.obj['verbose'] = verbose
    
    # Authenticate and create services
    authenticator = GmailAuthenticator(credentials)
    service = authenticator.authenticate()
    gmail_service = GmailService(service)
    
    ctx.obj['gmail_service'] = gmail_service
    ctx.obj['authenticator'] = authenticator
    # Pass credentials to processor for thread safety
    ctx.obj['processor'] = EmailProcessor(gmail_service, credentials=authenticator.get_credentials())


@cli.command()
@click.option('--limit', default=10, help='Number of emails to display')
@click.pass_context
def list(ctx, limit):
    """List emails with 'pending-unsubscribe' label"""
    gmail_service = ctx.obj['gmail_service']
    emails = gmail_service.get_emails_with_label(LABEL_PENDING, limit)
    
    if not emails:
        console.print("📭 No emails found with 'pending-unsubscribe' label", style="yellow")
        return
    
    console.print(f"\n📧 Found {len(emails)} emails pending unsubscription:\n", style="bold green")
    console.print("=" * 80)
    
    # Use Rich progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("•"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=4
    ) as progress:
        
        task = progress.add_task("[cyan]Loading emails...", total=len(emails))
        
        for i, email in enumerate(emails, 1):
            details = gmail_service.get_email_details(email['id'])
            if details:
                headers = extract_headers(details)
                subject = headers.get('Subject', 'No Subject')
                from_addr = headers.get('From', 'Unknown')
                list_unsub = headers.get('List-Unsubscribe', 'None')
                
                # Update progress bar description
                progress.update(task, description=f"[cyan]Loading email {i}/{len(emails)}")
                
                # Create formatted output
                email_info = Panel(
                    f"📨 Subject: {subject}\n"
                    f"👤 From: {from_addr}\n"
                    f"🔗 Unsubscribe: {'✅ Available' if list_unsub != 'None' else '❌ Not Available'}",
                    title=f"Email {i}",
                    expand=False
                )
                console.print(email_info)
                
                # Update progress
                progress.update(task, advance=1)
    
    console.print("\n" + "=" * 80)


@cli.command()
@click.option('--dry-run', is_flag=True, 
              help='Preview actions without making changes')
@click.option('--limit', default=0, 
              help='Process only N emails (0 for all)')
@click.option('--no-browser', is_flag=True, 
              help='Do not open browser for complex unsubscribes')
@click.option('--delay', default=DEFAULT_DELAY_SECONDS, 
              help='Delay in seconds between processing emails')
@click.option('--threads', default=DEFAULT_THREAD_COUNT, 
              help='Number of concurrent threads for processing')
@click.pass_context
def process(ctx, dry_run, limit, no_browser, delay, threads):
    """Process emails for unsubscription with threading"""
    gmail_service = ctx.obj['gmail_service']
    authenticator = ctx.obj['authenticator']
    
    if dry_run:
        console.print("🔍 DRY RUN MODE - No actual changes will be made\n", style="bold yellow")
    
    console.print(f"⚡ Using {threads} threads for processing\n", style="bold cyan")
    
    # Create processor with specified thread count and credentials
    processor = EmailProcessor(gmail_service, thread_count=threads, credentials=authenticator.get_credentials())
    
    # Get emails
    emails = gmail_service.get_emails_with_label(LABEL_PENDING, DEFAULT_MAX_RESULTS)
    
    if not emails:
        console.print("📭 No emails found with 'pending-unsubscribe' label", style="yellow")
        return
    
    # Limit number of emails to process
    if limit > 0:
        emails = emails[:limit]
    
    total = len(emails)
    console.print(f"📧 Processing {total} emails...\n", style="bold green")
    
    # Process emails with threading
    success_count, failed_count = processor.process_batch(
        emails, 
        dry_run=dry_run, 
        open_browser=not no_browser,
        delay=delay
    )
    
    # Final summary (already printed by processor)
    if dry_run:
        console.print("\n🔍 This was a dry run - no changes were made", style="yellow")


@cli.command()
@click.pass_context
def setup(ctx):
    """Setup guide for Gmail API credentials"""
    setup_text = Text()
    setup_text.append("🚀 Gmail Unsubscriber Setup Guide\n", style="bold cyan")
    setup_text.append("=" * 35 + "\n\n", style="cyan")
    
    setup_text.append("1️⃣  Enable Gmail API:\n", style="bold")
    setup_text.append("   • Go to https://console.cloud.google.com/\n")
    setup_text.append("   • Create a new project or select existing\n")
    setup_text.append("   • Enable Gmail API for the project\n\n")
    
    setup_text.append("2️⃣  Create OAuth 2.0 Credentials:\n", style="bold")
    setup_text.append("   • Go to APIs & Services > Credentials\n")
    setup_text.append("   • Click 'Create Credentials' > 'OAuth client ID'\n")
    setup_text.append("   • Choose 'Desktop app' as application type\n")
    setup_text.append("   • Download the credentials as 'credentials.json'\n\n")
    
    setup_text.append("3️⃣  Place credentials.json in the same directory as this script\n\n")
    
    setup_text.append("4️⃣  Run 'unsubscriber list' to authenticate\n\n")
    
    setup_text.append("5️⃣  In Gmail:\n", style="bold")
    setup_text.append("   • Create a label called 'pending-unsubscribe'\n")
    setup_text.append("   • Apply this label to emails you want to unsubscribe from\n\n")
    
    setup_text.append("6️⃣  Run 'unsubscriber process' to unsubscribe! 🎉\n\n")
    
    setup_text.append("💡 Pro tip: Use 'unsubscriber process --threads 16' for faster processing!\n", style="italic green")
    
    console.print(Panel(setup_text, expand=False))


@cli.command()
@click.pass_context
def stats(ctx):
    """Show statistics about processed emails"""
    gmail_service = ctx.obj['gmail_service']
    
    pending = gmail_service.get_emails_with_label(LABEL_PENDING, 1000)
    unsubscribed = gmail_service.get_emails_with_label('unsubscribed', 1000)
    
    stats_text = Text()
    stats_text.append("📊 Unsubscriber Statistics\n", style="bold cyan")
    stats_text.append("=" * 40 + "\n", style="cyan")
    stats_text.append(f"📧 Pending unsubscription: {len(pending)}\n", style="yellow")
    stats_text.append(f"✅ Successfully unsubscribed: {len(unsubscribed)}\n", style="green")
    stats_text.append(f"📈 Total processed: {len(pending) + len(unsubscribed)}\n", style="bold")
    stats_text.append("=" * 40, style="cyan")
    
    console.print(Panel(stats_text, title="Statistics", expand=False))