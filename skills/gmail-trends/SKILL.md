---
name: gmail-trends
description: >
  Trend analysis across time periods. Compares email activity across days,
  weeks, or months to surface seasonality, spikes, and long-term patterns.
---

# gmail-trends — Trend Analysis

## Purpose

Identify trends in email activity over time by comparing volumes across
days, weeks, or months to detect seasonality, spikes, and behavioral shifts.

## Trigger

- `/gmail trends year`
- `/gmail trends month`

## What It Reports

- Volume by day/week/month over the period
- Busiest and quietest periods
- Volume trend direction (increasing, stable, decreasing)
- Spike detection with context
- Year-over-year or month-over-month comparison
- Seasonality patterns

## Workflow

1. Fetch data for the period
2. Run `scripts/trend_analyzer.py` for time-series aggregation
3. Calculate moving averages and trend lines
4. Detect anomalies and spikes
5. Generate trend visualization data

## Output

- `GMAIL-REPORT-TRENDS.md`
