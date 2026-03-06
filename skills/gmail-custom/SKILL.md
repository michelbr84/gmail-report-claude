---
name: gmail-custom
description: >
  Custom date-range reports with mixed filters. Supports arbitrary start/end
  dates combined with any filter flags for fully flexible reporting.
---

# gmail-custom — Custom Date Range Reports

## Purpose

Generate reports for arbitrary date ranges with any combination of filters.
This is the most flexible reporting skill, supporting all filter options.

## Trigger

- `/gmail custom --from 2026-03-01 --to 2026-03-06`
- `/gmail custom --from 2026-03-01 --to 2026-03-06 --unread-only`
- `/gmail custom --from 2026-03-01 --to 2026-03-06 --include-spam`
- `/gmail custom --from 2026-03-01 --to 2026-03-06 --label "Work" --sender user@example.com`

## Supported Filters

All filters can be combined:

- `--from YYYY-MM-DD` — Start date (required)
- `--to YYYY-MM-DD` — End date (required)
- `--include-spam` / `--exclude-spam`
- `--unread-only` / `--read-only` / `--all-received`
- `--label "Name"` — Filter by Gmail label
- `--category <type>` — Filter by category
- `--sender <email>` — Filter by sender
- `--has-attachments` — Only messages with attachments

## Workflow

1. Parse `--from` and `--to` dates
2. Fetch data for the custom range
3. Apply all specified filters
4. Generate report using `templates/custom-report.md`

## Output

- `GMAIL-REPORT-CUSTOM.md`
