"""Gmail API integration module."""

import os
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.console import Console

console = Console()

# Gmail API scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.labels",
]


class GmailClient:
    """Gmail API client wrapper."""

    def __init__(self, credentials_path: Path):
        """Initialize Gmail client with credentials."""
        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Gmail API."""
        creds = None
        token_path = self.credentials_path.parent / "token.pickle"

        # Load existing token
        if token_path.exists():
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    console.print(f"[yellow]Token refresh failed: {e}[/yellow]")
                    creds = None

            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next run
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("gmail", "v1", credentials=creds)
        console.print("[green]✓ Gmail API authenticated successfully[/green]")

    def get_labels(self) -> Dict[str, str]:
        """Get all Gmail labels and return name->id mapping."""
        try:
            results = self.service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])
            return {label["name"]: label["id"] for label in labels}
        except HttpError as error:
            console.print(f"[red]Error getting labels: {error}[/red]")
            return {}

    def resolve_label_ids(self, label_names: List[str]) -> List[str]:
        """Convert label names to label IDs."""
        label_map = self.get_labels()
        label_ids = []

        for name in label_names:
            if name in label_map:
                label_ids.append(label_map[name])
            else:
                # Try case-insensitive match
                name_lower = name.lower()
                found = False
                for label_name, label_id in label_map.items():
                    if label_name.lower() == name_lower:
                        label_ids.append(label_id)
                        found = True
                        break

                if not found:
                    console.print(f"[yellow]Warning: Label '{name}' not found[/yellow]")

        return label_ids

    def list_messages(
        self,
        label_ids: List[str],
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List messages in specified labels."""
        try:
            query_params = {
                "userId": "me",
                "labelIds": label_ids,
                "includeSpamTrash": False,
            }

            if max_results:
                query_params["maxResults"] = max_results

            if page_token:
                query_params["pageToken"] = page_token

            return self.service.users().messages().list(**query_params).execute()
        except HttpError as error:
            console.print(f"[red]Error listing messages: {error}[/red]")
            return {"messages": []}

    def get_message(
        self, message_id: str, format: str = "full"
    ) -> Optional[Dict[str, Any]]:
        """Get a specific message by ID."""
        try:
            return (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format=format)
                .execute()
            )
        except HttpError as error:
            console.print(f"[red]Error getting message {message_id}: {error}[/red]")
            return None

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None,
    ) -> bool:
        """Send an email via Gmail API."""
        try:
            import base64
            from email.mime.text import MIMEText

            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject
            if from_email:
                message["from"] = from_email

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            send_message = {"raw": raw_message}

            result = (
                self.service.users()
                .messages()
                .send(userId="me", body=send_message)
                .execute()
            )

            console.print(f"[green]✓ Email sent to {to}[/green]")
            return True

        except HttpError as error:
            console.print(f"[red]Error sending email to {to}: {error}[/red]")
            return False

    def get_message_headers(self, message_id: str) -> Dict[str, str]:
        """Extract headers from a message."""
        message = self.get_message(message_id, format="metadata")
        if not message:
            return {}

        headers = {}
        payload = message.get("payload", {})

        for header in payload.get("headers", []):
            name = header.get("name", "").lower()
            value = header.get("value", "")
            headers[name] = value

        return headers

    def get_message_date(self, message_id: str) -> Optional[int]:
        """Get message date as UNIX timestamp."""
        message = self.get_message(message_id, format="minimal")
        if not message:
            return None

        # Gmail stores timestamp in milliseconds, convert to seconds
        internal_date = message.get("internalDate")
        if internal_date:
            return int(internal_date) // 1000

        return None
