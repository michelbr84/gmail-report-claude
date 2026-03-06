---
name: gmail-categories
description: >
  Gmail category analysis. Breaks down email across Primary, Promotions,
  Social, Updates, and Forums tabs to measure inbox composition.
---

# gmail-categories — Category Analysis

## Purpose

Analyze email distribution across Gmail's built-in categories (Primary,
Promotions, Social, Updates, Forums) to understand inbox composition.

## Trigger

- `/gmail categories month`
- Any command with `--category` filter

## What It Reports

- Email count per category
- Category percentages (pie chart data)
- Primary vs non-Primary ratio
- Category trends over time
- Actionable vs noise ratio

## Workflow

1. Fetch data for the period
2. Extract category labels from each message
3. Aggregate and compute distribution
4. Compare against typical patterns

## Output

- `GMAIL-REPORT-CATEGORIES.md`
