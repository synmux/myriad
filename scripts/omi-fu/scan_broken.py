"""Scan an Omi account for broken conversations, and optionally delete them.

A conversation counts as broken when it is more than 24 hours old and either:

1. its status never reached `completed` (`in_progress`, `processing` or `merging`), or
2. it is `completed`, but the server still reports it as being processed
   (`home_step` is `transcribing` or `writing_notes`).

Two options widen the match:

--discarded    also match conversations that Omi marked as discarded.
--no-summary   also match kept (not discarded) conversations whose summary is empty.

Nothing younger than 24 hours is ever matched.

Uses the app API, which needs a Firebase ID token. The developer API key is
rejected there, and the developer API hides every conversation that is not completed.

Usage:
    set -x __OMI_ID_TOKEN (pbpaste)                # a fresh token; it expires after one hour
    uv run scan_broken.py                          # report broken conversations
    uv run scan_broken.py --discarded --no-summary # report those as well
    uv run scan_broken.py --delete                 # delete every match permanently
"""

import argparse
import os
import sys
from collections import Counter
from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta
from functools import partial
from typing import Any

import requests

BASE_URL = "https://api.omi.me/v1/conversations"
TIMEOUT_SECONDS = 90
PAGE_SIZE = 100
# Younger conversations may still be recording, processing or settling into a longer one.
MINIMUM_AGE = timedelta(hours=24)
UNFINISHED_STATUSES = ("in_progress", "processing", "merging")
STILL_PROCESSING_HOME_STEPS = ("transcribing", "writing_notes")
# shortcut: no list returns status `failed`, so those rows are never scanned; probe by ID if one is suspected.
LISTABLE_STATUSES = (*UNFINISHED_STATUSES, "completed")

# One row from the app API list. The rows are unvalidated JSON, so their values stay untyped.
type Conversation = dict[str, Any]
type QueryParams = dict[str, str | int]
# Fetches one list page for the given query parameters: (rows, truncated by the server).
type Fetch = Callable[[QueryParams], tuple[list[Conversation], bool]]


def auth_headers() -> dict[str, str]:
    """
    Build the request headers from the Firebase ID token in __OMI_ID_TOKEN.

    Returns:
        dict[str, str]: Headers that authenticate against the app API.
    """
    id_token = os.environ.get("__OMI_ID_TOKEN")
    if not id_token:
        sys.exit(
            "Set __OMI_ID_TOKEN to a fresh Firebase ID token (it expires after one hour)."
        )
    return {"Authorization": f"Bearer {id_token}"}


def structured_text(conversation: Conversation, field: str) -> str:
    """
    Read one text field from a conversation's `structured` block.

    Args:
        conversation (Conversation): One row from the list.
        field (str): The field to read, such as `title`.

    Returns:
        str: The text, or an empty string when the block or the field is missing or null.
    """
    structured: dict[str, Any] = conversation.get("structured") or {}
    return structured.get(field) or ""


def cleanup_reason(
    conversation: Conversation,
    now: datetime,
    include_discarded: bool = False,
    include_no_summary: bool = False,
) -> str | None:
    """
    Decide whether a conversation row from the app API list should be cleaned up.

    Args:
        conversation (Conversation): One row from the list.
        now (datetime): The current time, timezone-aware.
        include_discarded (bool): Also match discarded conversations.
        include_no_summary (bool): Also match kept conversations with an empty summary.

    Returns:
        str | None: Why the conversation matches, or None when it should be left alone.
    """
    created_at = datetime.fromisoformat(conversation["created_at"])
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    if now - created_at <= MINIMUM_AGE:
        return None

    status = conversation.get("status")
    if status in UNFINISHED_STATUSES:
        return f"status is {status}"

    home_step = conversation.get("home_step")
    if status == "completed" and home_step in STILL_PROCESSING_HOME_STEPS:
        return f"completed but still {home_step}"

    if conversation.get("discarded"):
        return "discarded" if include_discarded else None

    if include_no_summary and not structured_text(conversation, "overview").strip():
        return "no summary"
    return None


def fetch_page(
    headers: dict[str, str], params: QueryParams
) -> tuple[list[Conversation], bool]:
    """
    Fetch one page of the conversation list.

    Args:
        headers (dict[str, str]): Headers from auth_headers().
        params (QueryParams): Query parameters for the list.

    Returns:
        tuple[list[Conversation], bool]: The rows, and whether the server truncated the page.
    """
    response = requests.get(
        BASE_URL, headers=headers, params=params, timeout=TIMEOUT_SECONDS
    )
    if response.status_code == 401:
        sys.exit("Token rejected (HTTP 401): it has probably expired.")
    response.raise_for_status()
    return (
        response.json(),
        response.headers.get("X-Omi-List-Truncated", "").lower() == "true",
    )


def list_conversations(status: str, fetch: Fetch) -> Iterator[Conversation]:
    """
    Yield every conversation with the given status once, discarded ones included.

    Args:
        status (str): One conversation status, such as `processing`.
        fetch (Fetch): Fetches one list page for the given query parameters.

    Raises:
        RuntimeError: The scan would be incomplete, so its result cannot be trusted.
    """
    seen_ids: set[str] = set()
    params: QueryParams = {
        "statuses": status,
        "include_discarded": "true",
        "limit": PAGE_SIZE,
    }
    while True:
        page, truncated = fetch(params)

        # `end_date` is inclusive, so the previous page's last row must come back.
        if "end_date" in params and not any(row["id"] in seen_ids for row in page):
            raise RuntimeError(
                f"The {status} list lost its place at {params['end_date']}; rows may have been skipped."
            )

        new_rows = [row for row in page if row["id"] not in seen_ids]
        for row in new_rows:
            seen_ids.add(row["id"])
            yield row

        if not truncated and len(page) < PAGE_SIZE:
            return
        if not new_rows:
            raise RuntimeError(
                f"The {status} list stopped making progress; the scan is incomplete."
            )
        # Page by date, newest first. Deep offsets run out of the server's read budget and come back truncated.
        params = params | {"end_date": page[-1]["created_at"]}


def delete_conversation(conversation_id: str, headers: dict[str, str]) -> bool:
    """
    Permanently delete one conversation.

    Args:
        conversation_id (str): The conversation's UUID.
        headers (dict[str, str]): Headers from auth_headers().

    Returns:
        bool: True when the server confirmed the deletion.
    """
    response = requests.delete(
        f"{BASE_URL}/{conversation_id}", headers=headers, timeout=TIMEOUT_SECONDS
    )
    if response.status_code == 401:
        sys.exit(
            "Token rejected (HTTP 401): it has probably expired. Stopped here; run again with a fresh token."
        )
    if response.ok:
        print(f"deleted       {conversation_id}")
        return True
    print(
        f"FAILED        {conversation_id} HTTP {response.status_code}: {response.text[:200]}"
    )
    return False


def main() -> int:
    """
    Scan every conversation, report the matches, and delete them with --delete.

    Returns:
        int: 0 on success, 1 when any delete failed.
    """
    parser = argparse.ArgumentParser(
        description="Find broken Omi conversations and optionally delete them."
    )
    parser.add_argument(
        "--discarded", action="store_true", help="also match discarded conversations"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="also match kept conversations with no summary",
    )
    parser.add_argument(
        "--delete", action="store_true", help="permanently delete every match"
    )
    arguments = parser.parse_args()

    headers = auth_headers()
    now = datetime.now(UTC)

    # The scan only lists. Fetching a `deferred` conversation by ID starts its processing.
    matches: dict[str, str] = {}
    scanned = 0
    for status in LISTABLE_STATUSES:
        for conversation in list_conversations(status, partial(fetch_page, headers)):
            scanned += 1
            reason = cleanup_reason(
                conversation, now, arguments.discarded, arguments.no_summary
            )
            if reason and conversation["id"] not in matches:
                matches[conversation["id"]] = reason
                title = structured_text(conversation, "title")
                print(
                    f"match         {conversation['id']} {conversation['created_at'][:10]} {reason} | {title[:40]}"
                )

    summary = ", ".join(
        f"{count} {reason}" for reason, count in Counter(matches.values()).most_common()
    )
    print(f"Scanned {scanned} conversations. Matches: {summary or 'none'}.")

    if not arguments.delete:
        if matches:
            print(
                "Scan only: nothing was deleted. Add --delete to delete these permanently."
            )
        return 0

    # Deleting waits until the scan has finished, so the list does not shift under the scan.
    failures = sum(
        not delete_conversation(conversation_id, headers) for conversation_id in matches
    )
    print(f"Deleted {len(matches) - failures} of {len(matches)}.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
