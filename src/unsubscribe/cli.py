"""Main CLI entry point for the unsubscribe tool."""

import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .gmail import GmailClient
from .processor import UnsubscribeProcessor
from .scanner import EmailScanner

console = Console()


@click.group()
@click.option(
    "--api-key",
    type=click.Path(exists=True, path_type=Path),
    help="Path to Gmail API credentials JSON file",
)
@click.pass_context
def cli(ctx: click.Context, api_key: Optional[Path]) -> None:
    """Gmail unsubscribe automation tool."""
    ctx.ensure_object(dict)

    # Determine credentials path
    if api_key:
        credentials_path = api_key
    elif os.getenv("GMAIL_API_KEY"):
        credentials_path = Path(os.getenv("GMAIL_API_KEY"))
    else:
        console.print(
            "[red]Error: No API key specified. Use --api-key or set GMAIL_API_KEY environment variable.[/red]"
        )
        ctx.exit(1)

    ctx.obj["credentials_path"] = credentials_path


@cli.command()
@click.option(
    "--labels",
    default="INBOX",
    help="Gmail labels to scan (comma-separated). Defaults to INBOX.",
)
@click.option(
    "--resume",
    type=click.Path(exists=True, path_type=Path),
    help="Resume scanning from an existing CSV file",
)
@click.pass_context
def scan(ctx: click.Context, labels: str, resume: Optional[Path]) -> None:
    """Scan Gmail for emails with List-Unsubscribe headers."""
    credentials_path = ctx.obj["credentials_path"]

    try:
        gmail_client = GmailClient(credentials_path)
        scanner = EmailScanner(gmail_client)

        # Parse labels
        label_list = [label.strip().strip('"') for label in labels.split(",")]

        if resume:
            console.print(f"[yellow]Resuming scan from {resume}[/yellow]")
            output_file = scanner.resume_scan(resume, label_list)
        else:
            console.print(
                f"[green]Starting new scan of labels: {', '.join(label_list)}[/green]"
            )
            output_file = scanner.scan_emails(label_list)

        console.print(f"[green]Scan completed! Results saved to: {output_file}[/green]")

    except Exception as e:
        console.print(f"[red]Error during scan: {e}[/red]")
        ctx.exit(1)


@cli.command()
@click.argument("csv_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--http-browser",
    is_flag=True,
    help="Open HTTP unsubscribe links in browser instead of making requests",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Resume processing, skipping already processed entries",
)
@click.option(
    "--yes",
    is_flag=True,
    help="Skip confirmation prompt",
)
@click.pass_context
def run(
    ctx: click.Context,
    csv_file: Path,
    http_browser: bool,
    resume: bool,
    yes: bool,
) -> None:
    """Process unsubscribe actions from CSV file."""
    credentials_path = ctx.obj["credentials_path"]

    try:
        gmail_client = GmailClient(credentials_path)
        processor = UnsubscribeProcessor(gmail_client, use_browser=http_browser)

        console.print(f"[green]Processing unsubscribe actions from: {csv_file}[/green]")

        if resume:
            console.print(
                "[yellow]Resume mode: skipping already processed entries[/yellow]"
            )

        results = processor.process_unsubscribes(csv_file, resume=resume)

        console.print("[green]Processing completed![/green]")
        console.print(f"  • Processed: {results['processed']}")
        console.print(f"  • Successful: {results['successful']}")
        console.print(f"  • Failed: {results['failed']}")
        console.print(f"  • Skipped: {results['skipped']}")

    except Exception as e:
        console.print(f"[red]Error during processing: {e}[/red]")
        ctx.exit(1)


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
