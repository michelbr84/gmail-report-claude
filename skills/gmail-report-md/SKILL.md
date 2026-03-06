---
name: gmail-report-md
description: >
  Markdown report generator. Takes analyzed data and produces a structured,
  well-formatted Markdown report suitable for Claude Code output, documentation,
  internal notes, and quick sharing.
---

# gmail-report-md — Markdown Report Generation

## Purpose

Transform analyzed Gmail data into a clean, structured Markdown report
that's ready for documentation, sharing, or archiving.

## When Used

Called at the end of any report workflow when output format is Markdown
(the default format).

## Report Structure

1. **Header** — Report title, period, filters used, generation date
2. **Executive Summary** — One-paragraph overview with key metrics
3. **Gmail Inbox Score** — Composite 0-100 score with breakdown
4. **Volume Analysis** — Total, daily average, peak days
5. **Unread Status** — Backlog depth and trend
6. **Sender Analysis** — Top senders table
7. **Label & Category Breakdown** — Distribution tables
8. **Spam Analysis** — Noise ratio and trends
9. **Response Behavior** — Reply latency stats
10. **Recommendations** — Prioritized action items

## Templates

Uses templates from `templates/` directory:
- `summary.md` for quick summaries
- `monthly-report.md` for monthly reports
- `yearly-report.md` for yearly reports
- `custom-report.md` for custom date ranges

## Output

- `GMAIL-REPORT-<period>.md`
