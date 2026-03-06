---
name: gmail-senders
description: >
  Sender analysis skill. Ranks senders by volume, identifies concentration
  risk, detects high-noise senders, and separates important contacts from
  clutter sources.
---

# gmail-senders — Sender Analysis

## Purpose

Rank and analyze senders to understand who dominates the inbox, identify
concentration risk, and separate high-value contacts from noise sources.

## Trigger

- `/gmail senders month`
- `/gmail senders year`
- Any command with `--sender` filter

## What It Reports

- Top 20 senders by volume
- Sender concentration (% from top 5 senders)
- High-noise senders (newsletters, automated)
- Important contacts vs clutter sources
- New senders in the period
- Sender activity trends

## Workflow

1. Fetch data for the period
2. Run `scripts/sender_ranker.py` for aggregation
3. Calculate concentration metrics
4. Classify senders (human, automated, newsletter, notification)

## Output

- `GMAIL-REPORT-SENDERS.md`
