---
name: gmail-report
description: >
  Full Gmail inbox report orchestration. Coordinates data collection, filtering,
  parallel analysis via subagents, score calculation, and final report generation.
  This is the main entry point for comprehensive inbox reports.
---

# gmail-report — Full Report Orchestration

## Purpose

Orchestrate a complete Gmail inbox report for a given period. This skill coordinates
all other sub-skills and subagents to produce a comprehensive analysis.

## Trigger

- `/gmail report today`
- `/gmail report week`
- `/gmail report month`
- `/gmail report year`

## Workflow

1. **Parse period** — Delegate to `gmail-period` to resolve date range
2. **Fetch data** — Run `scripts/fetch_gmail_data.py` for the resolved range
3. **Apply filters** — Run `scripts/filter_messages.py` with user-specified options
4. **Launch subagents** — Simultaneously launch:
   - `gmail-volume-analysis` (volume, spikes, seasonality)
   - `gmail-noise-analysis` (spam, clutter)
   - `gmail-sender-analysis` (sender ranking)
   - `gmail-organization-analysis` (labels, categories)
   - `gmail-response-analysis` (reply behavior)
5. **Collect results** — Aggregate findings from all subagents
6. **Calculate score** — Compute Gmail Inbox Score (0-100) using weighted methodology
7. **Generate report** — Use `gmail-report-md` or `gmail-report-pdf` template

## Scoring Weights

| Category | Weight |
|----------|--------|
| Inbox Health & Workload | 25% |
| Unread Backlog | 20% |
| Spam / Noise Ratio | 15% |
| Response Behavior | 15% |
| Sender Concentration | 10% |
| Label & Category Organization | 10% |
| Attachment / File Load | 5% |

## Output

- `GMAIL-REPORT-<period>.md` — Full markdown report
- Score: 0-100 composite Gmail Inbox Score
