"""Utility functions for the unsubscribe tool."""

import re
from urllib.parse import urlparse


def is_valid_email(email: str) -> bool:
    """Check if a string is a valid email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Check if a string is a valid HTTP/HTTPS URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in [
            "http",
            "https",
        ]
    except Exception:
        return False


def clean_email_address(email: str) -> str:
    """Clean and normalize email address."""
    if not email:
        return ""

    # Remove surrounding whitespace and quotes
    cleaned = email.strip().strip('"').strip("'")

    # Extract email from potential 'Name <email>' format
    email_match = re.search(r"<([^>]+)>", cleaned)
    if email_match:
        cleaned = email_match.group(1)

    return cleaned.lower()


def format_unsubscribe_action(unsubscribe_email: str, unsubscribe_url: str) -> str:
    """Suggest appropriate action based on available unsubscribe options."""
    has_email = bool(unsubscribe_email and is_valid_email(unsubscribe_email))
    has_url = bool(unsubscribe_url and is_valid_url(unsubscribe_url))

    if has_email and has_url:
        return "both (email: email, http: http, both: both)"
    elif has_email:
        return "email"
    elif has_url:
        return "http"
    else:
        return "none"


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
