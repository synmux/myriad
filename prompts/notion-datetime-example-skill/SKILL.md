---
name: notion-datetime
description: Insert the current date and time into a Notion document. Use when the user asks to timestamp a Notion page, log the current time, add a "last updated" entry, or insert datetime entries into Notion. Triggers on requests like "add the current time to my Notion page", "timestamp this document", or "log when I did this".
---

# Notion DateTime Skill

Insert formatted timestamps into Notion documents using the Notion MCP.

## Workflow

1. Run `scripts/format_datetime.py` to get the formatted timestamp
2. Use the Notion MCP to insert the timestamp into the target page

## Usage

```bash
# Default format (ISO 8601)
python scripts/format_datetime.py

# Specific format
python scripts/format_datetime.py --format human
python scripts/format_datetime.py --format iso
python scripts/format_datetime.py --format date-only
python scripts/format_datetime.py --format time-only

# Custom strftime format
python scripts/format_datetime.py --format custom --pattern "%A, %d %B %Y at %H:%M"
```

## Notion Integration

After obtaining the formatted timestamp, use the Notion MCP's `notion-update-page` tool to insert it. Common patterns:

**Append to page content:**

```plaintext
command: insert_content_after
selection_with_ellipsis: "<last paragraph>..."
new_str: "\n\n**Last updated:** {timestamp}"
```

**Update a property (for database pages):**

```plaintext
command: update_properties
properties: {"Last Updated": "{timestamp}"}
```

## Format Reference

See `references/datetime-formats.md` for format examples and use cases.
