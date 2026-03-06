---
name: gmail-summary
description: >
  Quick inbox summary without full deep analysis. Provides a fast snapshot of
  email volume, unread count, top senders, and key metrics for a given period.
---

# gmail-summary — Quick Inbox Summary

## Purpose

Generate a fast, lightweight snapshot of inbox activity without launching
full parallel analysis. Ideal for daily check-ins or quick status updates.

## Trigger

- `/gmail summary today`
- `/gmail summary week`

## What It Reports

- Total emails received in the period
- Unread vs read count
- Top 5 senders by volume
- Spam count (if `--include-spam`)
- Busiest hour / day of the period
- One-line health verdict

## Workflow

1. Parse period via `gmail-period`
2. Fetch data via `scripts/fetch_gmail_data.py`
3. Apply filters via `scripts/filter_messages.py`
4. Compute summary metrics directly (no subagents needed)
5. Output using `templates/summary.md`

## Output

- `GMAIL-REPORT-SUMMARY.md`
