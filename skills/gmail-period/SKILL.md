---
name: gmail-period
description: >
  Resolves time period arguments (today, week, month, year, custom date range)
  into concrete start and end dates for Gmail data queries.
---

# gmail-period — Period Resolution

## Purpose

Convert period keywords and date flags into concrete date ranges that other
skills and scripts can use for data fetching and filtering.

## Supported Periods

| Input | Resolved Range |
|-------|---------------|
| `today` | Start of today → now |
| `week` | 7 days ago → now |
| `month` | 30 days ago → now (or calendar month) |
| `year` | 365 days ago → now (or calendar year) |
| `--from YYYY-MM-DD --to YYYY-MM-DD` | Exact custom range |

## Logic

1. Parse the period keyword from user input
2. Calculate UTC start and end timestamps
3. Handle timezone awareness (default: user's local timezone)
4. Return structured date range for downstream use

## Used By

All skills that accept a `<period>` argument delegate to this skill for
date resolution before fetching or filtering data.
