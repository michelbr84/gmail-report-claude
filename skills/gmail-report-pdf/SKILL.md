---
name: gmail-report-pdf
description: >
  Professional PDF report generator. Creates a branded, chart-rich PDF
  with cover page, KPI tables, trend charts, sender rankings, and
  actionable recommendations. Ideal for client delivery and archival.
---

# gmail-report-pdf — PDF Report Generation

## Purpose

Generate a professional, print-ready PDF report with visual charts, tables,
and branding. Designed for client delivery, recurring reviews, and archival.

## Trigger

- `/gmail report-pdf`

## Prerequisites

Run a full report or individual analyses first to collect data.

## What the PDF Includes

- **Cover page** — Report title, period, generation date
- **Executive Summary** — Key metrics and Gmail Inbox Score
- **Score Breakdown** — Color-coded bar charts per category
- **Volume Analysis** — Daily/weekly volume charts
- **Sender Rankings** — Top senders table with volume bars
- **Label & Category Breakdown** — Pie charts and distribution tables
- **Spam vs Inbox** — Comparison chart
- **Unread Backlog** — Trend line chart
- **Response Time** — Latency distribution
- **Recommendations** — Prioritized action items
- **Methodology** — How scores are calculated

## Workflow

1. Collect all analysis data into a JSON structure
2. Execute: `python3 scripts/generate_pdf_report.py data.json GMAIL-REPORT.pdf`
3. The script uses `reportlab` and `matplotlib` for chart generation

## Output

- `GMAIL-REPORT.pdf`
