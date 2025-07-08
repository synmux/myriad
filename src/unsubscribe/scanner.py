"""Email scanner for extracting List-Unsubscribe headers."""

import csv
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd
from rich.console import Console
from tqdm import tqdm

from .gmail import GmailClient

console = Console()


class EmailScanner:
    """Scanner for extracting unsubscribe information from emails."""

    def __init__(self, gmail_client: GmailClient):
        """Initialize scanner with Gmail client."""
        self.gmail_client = gmail_client

    def _generate_filename(self) -> Path:
        """Generate timestamped filename for CSV output."""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        return Path(f"emails_{timestamp}.csv")

    def _parse_unsubscribe_header(
        self, header_value: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """Parse List-Unsubscribe header to extract email and/or URL."""
        if not header_value:
            return None, None

        unsubscribe_email = None
        unsubscribe_url = None

        # Extract email addresses (mailto: links)
        email_pattern = r"<mailto:([^>]+)>"
        email_matches = re.findall(email_pattern, header_value, re.IGNORECASE)
        if email_matches:
            unsubscribe_email = email_matches[0]

        # Extract HTTP/HTTPS URLs
        url_pattern = r"<(https?://[^>]+)>"
        url_matches = re.findall(url_pattern, header_value, re.IGNORECASE)
        if url_matches:
            unsubscribe_url = url_matches[0]

        return unsubscribe_email, unsubscribe_url

    def _extract_sender_info(self, headers: Dict[str, str]) -> Tuple[str, str]:
        """Extract sender email and name from headers."""
        from_header = headers.get("from", "")

        # Parse "Name <email@domain.com>" format
        email_pattern = r"<([^>]+)>"
        email_match = re.search(email_pattern, from_header)

        if email_match:
            email = email_match.group(1)
            name = from_header.split("<")[0].strip().strip('"')
        else:
            # Just an email address
            email = from_header.strip()
            name = ""

        return email, name

    def scan_emails(self, label_names: List[str]) -> Path:
        """Scan emails in specified labels for List-Unsubscribe headers."""
        # Resolve label names to IDs
        label_ids = self.gmail_client.resolve_label_ids(label_names)
        if not label_ids:
            raise ValueError("No valid labels found")

        console.print(f"[blue]Scanning labels: {', '.join(label_names)}[/blue]")

        output_file = self._generate_filename()
        seen_message_ids: Set[str] = set()

        # Prepare CSV
        fieldnames = [
            "from_address",
            "sender_name",
            "email_id",
            "email_date",
            "unsubscribe_link",
            "unsubscribe_email",
            "action",
            "processed",
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            page_token = None
            processed_count = 0
            found_count = 0

            # Initialize tqdm without total (no pre-count)
            with tqdm(desc="Scanning messages", unit="msg") as pbar:

                while True:
                    # Get batch of messages
                    result = self.gmail_client.list_messages(
                        label_ids, max_results=100, page_token=page_token
                    )

                    messages = result.get("messages", [])
                    if not messages:
                        break

                    # Process each message
                    for message in messages:
                        message_id = message["id"]

                        # Skip duplicates
                        if message_id in seen_message_ids:
                            continue
                        seen_message_ids.add(message_id)

                        # Get message headers and date
                        headers = self.gmail_client.get_message_headers(message_id)
                        email_date = self.gmail_client.get_message_date(message_id)

                        # Check for List-Unsubscribe header
                        unsubscribe_header = headers.get("list-unsubscribe", "")

                        if unsubscribe_header:
                            # Parse unsubscribe info
                            unsubscribe_email, unsubscribe_url = (
                                self._parse_unsubscribe_header(unsubscribe_header)
                            )

                            # Extract sender info
                            from_address, sender_name = self._extract_sender_info(
                                headers
                            )

                            # Write to CSV
                            writer.writerow(
                                {
                                    "from_address": from_address,
                                    "sender_name": sender_name,
                                    "email_id": message_id,
                                    "email_date": email_date or "",
                                    "unsubscribe_link": unsubscribe_url or "",
                                    "unsubscribe_email": unsubscribe_email or "",
                                    "action": "",
                                    "processed": "",
                                }
                            )

                            found_count += 1

                        processed_count += 1

                        # Update progress bar with current stats
                        pbar.set_description(
                            f"Scanned {processed_count} messages, found {found_count} unsubscribe"
                        )
                        pbar.update(1)

                    # Check for next page
                    page_token = result.get("nextPageToken")
                    if not page_token:
                        break

                    # Rate limiting
                    time.sleep(0.1)

                # Final description
                pbar.set_description(
                    f"✓ Scanned {processed_count} messages, found {found_count} unsubscribe"
                )

        console.print(
            f"[green]✓ Found {found_count} emails with unsubscribe information[/green]"
        )
        return output_file

    def resume_scan(self, existing_csv: Path, label_names: List[str]) -> Path:
        """Resume scanning from existing CSV file."""
        # Load existing data
        try:
            df = pd.read_csv(existing_csv)
            existing_ids = set(df["email_id"].tolist())
            console.print(
                f"[blue]Loaded {len(existing_ids)} existing entries from {existing_csv}[/blue]"
            )
        except Exception as e:
            console.print(f"[red]Error reading existing CSV: {e}[/red]")
            raise

        # Resolve label names to IDs
        label_ids = self.gmail_client.resolve_label_ids(label_names)
        if not label_ids:
            raise ValueError("No valid labels found")

        console.print(f"[blue]Resuming scan of labels: {', '.join(label_names)}[/blue]")

        new_entries = 0

        # Open CSV in append mode
        with open(existing_csv, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "from_address",
                "sender_name",
                "email_id",
                "email_date",
                "unsubscribe_link",
                "unsubscribe_email",
                "action",
                "processed",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            page_token = None
            checked_count = 0

            # Initialize tqdm for resume
            with tqdm(desc="Resuming scan", unit="msg") as pbar:

                while True:
                    # Get batch of messages
                    result = self.gmail_client.list_messages(
                        label_ids, max_results=100, page_token=page_token
                    )

                    messages = result.get("messages", [])
                    if not messages:
                        break

                    # Process each message
                    for message in messages:
                        message_id = message["id"]

                        # Skip if already processed
                        if message_id in existing_ids:
                            continue

                        # Get message headers and date
                        headers = self.gmail_client.get_message_headers(message_id)
                        email_date = self.gmail_client.get_message_date(message_id)

                        # Check for List-Unsubscribe header
                        unsubscribe_header = headers.get("list-unsubscribe", "")

                        if unsubscribe_header:
                            # Parse unsubscribe info
                            unsubscribe_email, unsubscribe_url = (
                                self._parse_unsubscribe_header(unsubscribe_header)
                            )

                            # Extract sender info
                            from_address, sender_name = self._extract_sender_info(
                                headers
                            )

                            # Write to CSV
                            writer.writerow(
                                {
                                    "from_address": from_address,
                                    "sender_name": sender_name,
                                    "email_id": message_id,
                                    "email_date": email_date or "",
                                    "unsubscribe_link": unsubscribe_url or "",
                                    "unsubscribe_email": unsubscribe_email or "",
                                    "action": "",
                                    "processed": "",
                                }
                            )

                            new_entries += 1

                        checked_count += 1

                        # Update progress
                        pbar.set_description(
                            f"Checked {checked_count} new messages, found {new_entries} new entries"
                        )
                        pbar.update(1)

                    # Check for next page
                    page_token = result.get("nextPageToken")
                    if not page_token:
                        break

                    # Rate limiting
                    time.sleep(0.1)

                # Final description
                pbar.set_description(
                    f"✓ Resume complete: {new_entries} new entries added"
                )

        console.print(
            f"[green]✓ Added {new_entries} new entries to {existing_csv}[/green]"
        )
        return existing_csv
