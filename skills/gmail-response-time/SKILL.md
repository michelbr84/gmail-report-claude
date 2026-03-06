---
name: gmail-response-time
description: >
  Response time analysis. Estimates reply latency, identifies fastest and
  slowest response windows, detects conversations needing follow-up,
  and tracks whether response behavior is improving or worsening.
---

# gmail-response-time — Response Time Analysis

## Purpose

Estimate reply behavior by analyzing sent-message timestamps relative to
received messages in the same thread, identifying response patterns.

## Trigger

- `/gmail response-time week`
- `/gmail response-time month`

## What It Reports

- Average reply latency
- Median reply time
- Fastest and slowest response windows
- Response time by day of week / hour
- Conversations likely needing follow-up
- Trend: response times improving or worsening

## Workflow

1. Fetch data for the period (both inbox and sent)
2. Run `scripts/response_time_analyzer.py` to match replies to originals
3. Calculate latency statistics
4. Identify follow-up-needed threads

## Output

- `GMAIL-REPORT-RESPONSE-TIME.md`
