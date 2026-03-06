---
name: gmail-spam
description: >
  Spam analysis skill. Measures spam volume, identifies spam trends,
  compares spam vs inbox ratio, and helps users understand how much
  of their incoming email is noise.
---

# gmail-spam — Spam Analysis

## Purpose

Analyze spam patterns to understand what proportion of incoming email is
noise versus actionable communication.

## Trigger

- `/gmail spam week`
- `/gmail spam month`
- Any command with `--include-spam` flag

## What It Reports

- Spam count in the period
- Spam as percentage of total incoming
- Spam trend (increasing or decreasing)
- Top spam senders / domains
- Spam by category (promotions vs actual spam)
- Comparison: inbox vs spam volume

## Workflow

1. Fetch data for the period (including spam folder)
2. Separate spam from inbox messages
3. Aggregate spam metrics and patterns
4. Generate spam analysis report

## Output

- `GMAIL-REPORT-SPAM.md`
