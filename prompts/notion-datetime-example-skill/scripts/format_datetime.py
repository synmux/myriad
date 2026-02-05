#!/usr/bin/env python3
"""
Format current datetime for insertion into Notion documents.

Provides consistent, tested datetime formatting to avoid regenerating
formatting logic on each invocation.
"""

import argparse
from datetime import datetime, timezone

FORMATS = {
    "iso": "%Y-%m-%dT%H:%M:%S%z",
    "human": "%d %B %Y at %H:%M",
    "date-only": "%Y-%m-%d",
    "time-only": "%H:%M:%S",
    "compact": "%Y%m%d_%H%M%S",
    "notion-date": "%Y-%m-%d",  # Notion's native date format
}


def get_formatted_datetime(format_name: str, pattern: str | None = None) -> str:
    """Return current datetime in the specified format."""
    now = datetime.now(timezone.utc).astimezone()

    if format_name == "custom" and pattern:
        return now.strftime(pattern)

    if format_name not in FORMATS:
        raise ValueError(
            f"Unknown format: {format_name}. Available: {list(FORMATS.keys())}"
        )

    return now.strftime(FORMATS[format_name])


def main():
    parser = argparse.ArgumentParser(
        description="Format current datetime for Notion insertion"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=list(FORMATS.keys()) + ["custom"],
        default="iso",
        help="Output format (default: iso)",
    )
    parser.add_argument(
        "--pattern", "-p", help="Custom strftime pattern (requires --format custom)"
    )

    args = parser.parse_args()

    if args.format == "custom" and not args.pattern:
        parser.error("--pattern required when using --format custom")

    print(get_formatted_datetime(args.format, args.pattern))


if __name__ == "__main__":
    main()
