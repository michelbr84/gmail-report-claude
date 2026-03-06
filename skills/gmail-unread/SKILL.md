---
name: gmail-unread
description: >
  Analyzes unread email patterns. Filters to show only unread messages,
  measures backlog depth, identifies neglected threads, and tracks whether
  the unread count is growing or shrinking over time.
---

# gmail-unread — Unread Email Analysis

## Purpose

Focus exclusively on unread emails to measure backlog health, identify
neglected conversations, and track whether inbox processing is keeping up
with incoming volume.

## Trigger

- `/gmail unread today`
- `/gmail unread week`
- Any command with `--unread-only` flag

## What It Reports

- Total unread count in the period
- Unread as percentage of total received
- Oldest unread message age
- Unread by label / category
- Unread trend (growing or shrinking vs previous period)
- Top senders with unread messages

## Workflow

1. Fetch data for the period
2. Apply `--unread-only` filter via `scripts/filter_messages.py`
3. Aggregate unread metrics
4. Compare against previous period for trend detection

## Output

- `GMAIL-REPORT-UNREAD.md`
