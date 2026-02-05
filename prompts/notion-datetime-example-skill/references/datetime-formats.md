# DateTime Format Reference

## Built-in Formats

| Format        | Example Output            | Use Case                        |
| ------------- | ------------------------- | ------------------------------- |
| `iso`         | 2025-02-03T14:30:00+00:00 | Machine-readable, sorting, APIs |
| `human`       | 03 February 2025 at 14:30 | User-facing timestamps          |
| `date-only`   | 2025-02-03                | Date without time               |
| `time-only`   | 14:30:00                  | Time without date               |
| `compact`     | 20250203_143000           | Filenames, IDs                  |
| `notion-date` | 2025-02-03                | Notion date property format     |

## Custom Patterns

Common strftime patterns for `--format custom --pattern`:

| Pattern             | Output                   | Notes                  |
| ------------------- | ------------------------ | ---------------------- |
| `%A, %d %B %Y`      | Monday, 03 February 2025 | Full weekday and month |
| `%d/%m/%Y %H:%M`    | 03/02/2025 14:30         | UK format              |
| `%m/%d/%Y %I:%M %p` | 02/03/2025 02:30 PM      | US format with 12-hour |
| `%Y-W%W`            | 2025-W05                 | ISO week number        |

## Notion Considerations

- **Rich text blocks**: Any format works, inserted as plain text
- **Date properties**: Use `notion-date` format for compatibility
- **Inline mentions**: Notion MCP handles @-mentions separately; this skill is for plain text timestamps
