"""Unsubscribe processor for handling unsubscribe actions."""

import time
import webbrowser
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import requests
from rich.console import Console
from rich.prompt import Confirm
from tqdm import tqdm

from .gmail import GmailClient

console = Console()


class UnsubscribeProcessor:
    """Processor for handling unsubscribe actions."""

    def __init__(self, gmail_client: GmailClient, use_browser: bool = False):
        """Initialize processor with Gmail client."""
        self.gmail_client = gmail_client
        self.use_browser = use_browser
        self.session = requests.Session()

        # Set a reasonable user agent
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def _process_email_unsubscribe(
        self, unsubscribe_email: str, from_address: str, sender_name: str
    ) -> bool:
        """Send unsubscribe email."""
        subject = "Unsubscribe Request"
        body = f"""Please unsubscribe this email address from your mailing list.

This is an automated unsubscribe request.

Original sender: {sender_name} <{from_address}>
"""

        try:
            success = self.gmail_client.send_email(
                to=unsubscribe_email, subject=subject, body=body
            )

            if success:
                console.print(
                    f"[green]✓ Sent unsubscribe email to {unsubscribe_email}[/green]"
                )
            else:
                console.print(
                    f"[red]✗ Failed to send unsubscribe email to {unsubscribe_email}[/red]"
                )

            return success

        except Exception as e:
            console.print(
                f"[red]✗ Error sending email to {unsubscribe_email}: {e}[/red]"
            )
            return False

    def _process_http_unsubscribe(
        self, unsubscribe_url: str, from_address: str
    ) -> bool:
        """Process HTTP unsubscribe link."""
        if self.use_browser:
            try:
                console.print(f"[blue]Opening {unsubscribe_url} in browser...[/blue]")
                webbrowser.open(unsubscribe_url)
                return True
            except Exception as e:
                console.print(
                    f"[red]✗ Error opening browser for {unsubscribe_url}: {e}[/red]"
                )
                return False
        else:
            try:
                console.print(
                    f"[blue]Making HTTP request to {unsubscribe_url}...[/blue]"
                )

                # Make GET request first
                response = self.session.get(
                    unsubscribe_url, timeout=30, allow_redirects=True
                )

                if response.status_code == 200:
                    console.print(
                        f"[green]✓ HTTP unsubscribe request successful for {from_address}[/green]"
                    )
                    return True
                elif response.status_code in [301, 302, 303, 307, 308]:
                    console.print(
                        f"[yellow]⚠ Redirect response ({response.status_code}) for {unsubscribe_url}[/yellow]"
                    )
                    return True  # Redirects are often normal for unsubscribe links
                else:
                    console.print(
                        f"[red]✗ HTTP error {response.status_code} for {unsubscribe_url}[/red]"
                    )
                    return False

            except requests.exceptions.Timeout:
                console.print(f"[red]✗ Timeout accessing {unsubscribe_url}[/red]")
                return False
            except requests.exceptions.RequestException as e:
                console.print(f"[red]✗ Request error for {unsubscribe_url}: {e}[/red]")
                return False
            except Exception as e:
                console.print(
                    f"[red]✗ Unexpected error for {unsubscribe_url}: {e}[/red]"
                )
                return False

    def process_unsubscribes(
        self, csv_file: Path, resume: bool = False
    ) -> Dict[str, int]:
        """Process unsubscribe actions from CSV file."""
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            console.print(f"[red]Error reading CSV file: {e}[/red]")
            raise

        # Filter rows that have actions
        if resume:
            # Skip already processed entries
            action_rows = df[
                (df["action"].notna())
                & (df["action"] != "")
                & ((df["processed"].isna()) | (df["processed"] == ""))
            ]
        else:
            action_rows = df[(df["action"].notna()) & (df["action"] != "")]

        if action_rows.empty:
            console.print("[yellow]No actions to process in CSV file[/yellow]")
            return {"processed": 0, "successful": 0, "failed": 0, "skipped": 0}

        console.print(f"[blue]Found {len(action_rows)} entries to process[/blue]")

        if not resume:
            # Show warning about processing actions
            console.print(
                "\n[yellow]⚠ WARNING: This will perform unsubscribe actions![/yellow]"
            )
            if self.use_browser:
                console.print(
                    "[blue]Browser mode: Will open unsubscribe links in your default browser[/blue]"
                )
            else:
                console.print(
                    "[blue]HTTP mode: Will make automated requests to unsubscribe links[/blue]"
                )

            console.print(
                f"[blue]Email mode: Will send unsubscribe emails via Gmail[/blue]"
            )

            if not Confirm.ask("\n[bold]Proceed with processing?[/bold]"):
                console.print("[yellow]Processing cancelled by user[/yellow]")
                return {"processed": 0, "successful": 0, "failed": 0, "skipped": 0}

        results = {"processed": 0, "successful": 0, "failed": 0, "skipped": 0}

        with tqdm(
            total=len(action_rows), desc="Processing unsubscribe actions", unit="action"
        ) as pbar:

            for idx, row in action_rows.iterrows():
                action = str(row["action"]).strip().lower()
                from_address = row["from_address"]
                sender_name = row.get("sender_name", "")
                unsubscribe_email = row.get("unsubscribe_email", "")
                unsubscribe_link = row.get("unsubscribe_link", "")

                pbar.set_description(f"Processing {from_address[:30]}...")

                success = False

                if action == "email" and unsubscribe_email:
                    success = self._process_email_unsubscribe(
                        unsubscribe_email, from_address, sender_name
                    )
                elif action == "http" and unsubscribe_link:
                    success = self._process_http_unsubscribe(
                        unsubscribe_link, from_address
                    )
                elif action == "both":
                    # Try both email and HTTP
                    email_success = False
                    http_success = False

                    if unsubscribe_email:
                        email_success = self._process_email_unsubscribe(
                            unsubscribe_email, from_address, sender_name
                        )

                    if unsubscribe_link:
                        http_success = self._process_http_unsubscribe(
                            unsubscribe_link, from_address
                        )

                    success = email_success or http_success
                else:
                    console.print(
                        f"[yellow]⚠ Skipping {from_address}: invalid action '{action}' or missing unsubscribe info[/yellow]"
                    )
                    results["skipped"] += 1
                    pbar.update(1)
                    continue

                # Update CSV with processed status
                df.loc[idx, "processed"] = "True" if success else "Failed"

                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1

                results["processed"] += 1
                pbar.update(1)

                # Rate limiting
                time.sleep(1)

        # Save updated CSV
        try:
            df.to_csv(csv_file, index=False)
            console.print(f"[green]✓ Updated CSV file: {csv_file}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving CSV file: {e}[/red]")

        return results
