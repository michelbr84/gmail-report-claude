---
name: gmail-labels
description: >
  Label distribution analysis. Breaks down email volume by Gmail labels
  to show how the inbox is organized and which labels receive the most traffic.
---

# gmail-labels — Label Distribution Analysis

## Purpose

Analyze how email is distributed across Gmail labels to understand inbox
organization effectiveness and identify high-traffic label areas.

## Trigger

- `/gmail labels month`
- `/gmail labels year`
- Any command with `--label` filter

## What It Reports

- Email count per label
- Labels ranked by volume
- Unlabeled email percentage
- Multi-labeled messages
- Label usage trends over time
- Recommendations for label organization

## Workflow

1. Fetch data for the period
2. Extract label metadata from each message
3. Aggregate counts per label
4. Calculate distribution percentages

## Output

- `GMAIL-REPORT-LABELS.md`
