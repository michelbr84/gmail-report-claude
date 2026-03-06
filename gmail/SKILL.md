---
name: gmail
description: >
  Gmail-first reporting skill suite. Analyzes inbox activity by day, week, month,
  year, or custom date range with flexible filters for unread messages, spam
  inclusion, labels, categories, senders, attachments, and response behavior.
  Generates structured reports in Markdown or PDF. Use when user says "gmail",
  "report", "inbox", "email", "unread", "spam", "senders", "labels", "response time",
  "trends", or any Gmail reporting request.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

# Gmail Reports — Claude Code Skill Suite (March 2026)

> **Philosophy:** Gmail-first, reporting-powered. Turn raw inbox data into
> clear, client-ready or personal productivity reports.

---

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `/gmail report today` | Full report for today's emails |
| `/gmail report week` | Full report for the last 7 days |
| `/gmail report month` | Full report for the current or last 30 days |
| `/gmail report year` | Full report for the current or last 12 months |
| `/gmail summary today` | Fast snapshot of volume, unread count, and top senders |
| `/gmail summary week` | Weekly summary without full deep analysis |
| `/gmail unread today` | Report only unread emails from today |
| `/gmail unread week` | Report only unread emails from the week |
| `/gmail spam week` | Analyze spam volume and spam trends for the week |
| `/gmail senders month` | Rank top senders for the month |
| `/gmail labels month` | Break down email volume by Gmail labels |
| `/gmail categories month` | Analyze Primary, Promotions, Social, Updates, and Forums |
| `/gmail attachments month` | Report attachment-heavy traffic and file volume |
| `/gmail response-time week` | Estimate reply behavior and response latency |
| `/gmail trends year` | Compare activity across months over the year |
| `/gmail custom --from YYYY-MM-DD --to YYYY-MM-DD` | Custom date range report |
| `/gmail organize month` | Analyze unlabeled emails and suggest label taxonomy |
| `/gmail suggest-labels month` | Alias for `/gmail organize` |
| `/gmail report-pdf` | Generate a professional PDF report with charts and tables |

### Common Filters

- `--include-spam` / `--exclude-spam`
- `--unread-only` / `--read-only` / `--all-received`
- `--label "Work"`
- `--category promotions`
- `--sender someone@example.com`
- `--has-attachments`
- `--from YYYY-MM-DD` / `--to YYYY-MM-DD`
- `--pdf` (generate PDF version)
- `--pt` (output in Portuguese)

---

## Orchestration Logic

### Full Report (`/gmail report <period>`)

**Phase 1: Data Collection (Sequential)**
1. **Detect data source** — Check availability in this order:
   - MCP Gmail tools available → use directly (no credentials needed)
   - `credentials.json` present → run `scripts/fetch_gmail_data.py` (OAuth flow)
   - Exported mailbox file provided → load JSON/CSV/MBOX directly
2. Fetch messages for the requested period
3. Apply selected filters (unread, spam, label, sender, category, attachments)

**Phase 2: Parallel Analysis (Delegate to Subagents)**
Launch these 5 subagents simultaneously:

| Subagent | File | Responsibility |
|----------|------|---------------|
| gmail-volume-analysis | `agents/gmail-volume-analysis.md` | Volume, spikes, and seasonality |
| gmail-noise-analysis | `agents/gmail-noise-analysis.md` | Spam, low-value mail, clutter patterns |
| gmail-sender-analysis | `agents/gmail-sender-analysis.md` | Sender ranking and concentration |
| gmail-organization-analysis | `agents/gmail-organization-analysis.md` | Labels, categories, inbox structure |
| gmail-response-analysis | `agents/gmail-response-analysis.md` | Response behavior and follow-up patterns |

**Phase 3: Synthesis (Sequential)**
1. Collect all subagent reports
2. Calculate composite Gmail Inbox Score (0-100)
3. Generate prioritized findings and recommendations
4. Output client-ready report (Markdown or PDF)

### Scoring Methodology

| Category | Weight |
|----------|--------|
| Inbox Health & Workload | 25% |
| Unread Backlog | 20% |
| Spam / Noise Ratio | 15% |
| Sender Concentration | 10% |
| Response Behavior | 15% |
| Label & Category Organization | 10% |
| Attachment / File Load | 5% |

---

## Sub-Skills (15 Specialized Components)

| # | Skill | Directory | Purpose |
|---|-------|-----------|---------| 
| 1 | gmail-report | `skills/gmail-report/` | Full report orchestration and scoring |
| 2 | gmail-summary | `skills/gmail-summary/` | Quick inbox summary |
| 3 | gmail-period | `skills/gmail-period/` | Day/week/month/year/custom range handling |
| 4 | gmail-unread | `skills/gmail-unread/` | Unread-only filtering and analysis |
| 5 | gmail-spam | `skills/gmail-spam/` | Spam inclusion/exclusion analysis |
| 6 | gmail-senders | `skills/gmail-senders/` | Top senders and sender concentration |
| 7 | gmail-labels | `skills/gmail-labels/` | Label distribution analysis (descriptive) |
| 8 | gmail-categories | `skills/gmail-categories/` | Promotions/Social/Primary/etc. analysis |
| 9 | gmail-attachments | `skills/gmail-attachments/` | Attachment volume and file pattern analysis |
| 10 | gmail-response-time | `skills/gmail-response-time/` | Reply speed and follow-up behavior |
| 11 | gmail-trends | `skills/gmail-trends/` | Trend lines across days, weeks, months |
| 12 | gmail-custom | `skills/gmail-custom/` | Custom date-range reports with mixed filters |
| 13 | gmail-report-md | `skills/gmail-report-md/` | Markdown report generation |
| 14 | gmail-report-pdf | `skills/gmail-report-pdf/` | Professional PDF report with charts |
| 15 | gmail-organize | `skills/gmail-organize/` | Inbox organization advisor (prescriptive) |

---

## Subagents (5 Parallel Workers)

| Agent | File | Skills Used |
|-------|------|-------------|
| gmail-volume-analysis | `agents/gmail-volume-analysis.md` | gmail-period, gmail-report |
| gmail-noise-analysis | `agents/gmail-noise-analysis.md` | gmail-spam |
| gmail-sender-analysis | `agents/gmail-sender-analysis.md` | gmail-senders |
| gmail-organization-analysis | `agents/gmail-organization-analysis.md` | gmail-labels, gmail-categories, gmail-organize |
| gmail-response-analysis | `agents/gmail-response-analysis.md` | gmail-response-time |

---

## Output Files

| Command | Output File |
|---------|-------------|
| `/gmail report` | `GMAIL-REPORT-<period>.md` |
| `/gmail summary` | `GMAIL-REPORT-SUMMARY.md` |
| `/gmail unread` | `GMAIL-REPORT-UNREAD.md` |
| `/gmail spam` | `GMAIL-REPORT-SPAM.md` |
| `/gmail senders` | `GMAIL-REPORT-SENDERS.md` |
| `/gmail labels` | `GMAIL-REPORT-LABELS.md` |
| `/gmail categories` | `GMAIL-REPORT-CATEGORIES.md` |
| `/gmail attachments` | `GMAIL-REPORT-ATTACHMENTS.md` |
| `/gmail response-time` | `GMAIL-REPORT-RESPONSE-TIME.md` |
| `/gmail trends` | `GMAIL-REPORT-TRENDS.md` |
| `/gmail custom` | `GMAIL-REPORT-CUSTOM.md` |
| `/gmail organize` | `GMAIL-REPORT-ORGANIZE.md` |
| `/gmail report-pdf` | `GMAIL-REPORT.pdf` |

---

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `scripts/fetch_gmail_data.py` | Gmail API authentication, message retrieval, and normalization |
| `scripts/filter_messages.py` | Date, spam, unread, label, category, and sender filtering |
| `scripts/sender_ranker.py` | Sender aggregation, ranking, and concentration analysis |
| `scripts/trend_analyzer.py` | Time-series analysis across periods |
| `scripts/response_time_analyzer.py` | Reply latency estimation and follow-up tracking |
| `scripts/organization_analyzer.py` | Inbox clustering, label suggestion, and organization score |
| `scripts/generate_pdf_report.py` | Professional PDF report with charts, tables, and scoring |

### Script Usage

```bash
# Fetch Gmail data for a period
python3 ~/.claude/skills/gmail/scripts/fetch_gmail_data.py --period month --output data.json

# Filter messages
python3 ~/.claude/skills/gmail/scripts/filter_messages.py data.json --unread-only --exclude-spam

# Generate PDF report
python3 ~/.claude/skills/gmail/scripts/generate_pdf_report.py data.json GMAIL-REPORT.pdf
```

---

## Report Templates

Templates in `templates/` provide consistent report structure:

| Template | Purpose |
|----------|---------|
| `summary.md` | Executive summary template |
| `monthly-report.md` | Monthly report template |
| `yearly-report.md` | Yearly report template |
| `custom-report.md` | Custom date range template |
| `organization-report.md` | Inbox organization advisor template |

---

## Data Sources

The skill detects the best available data source automatically, in priority order:

### Mode 1 — MCP Gmail (Default, no credentials needed)

If Claude has an active Gmail MCP connection, all data is fetched via MCP tools directly.
No `credentials.json`, no `token.json`, no OAuth flow required.

| MCP Tool | Purpose |
|----------|---------|
| `gmail_search_messages` | Fetch messages by period, label, read status, spam |
| `gmail_read_message` | Read individual message details |
| `gmail_read_thread` | Group messages into threads for response time analysis |
| `gmail_list_labels` | Enumerate user labels for label/category breakdown |
| `gmail_get_profile` | Retrieve account email for sender identification |

### Mode 2 — Gmail API via Python (Fallback)

Used when MCP is not available. Requires `credentials.json` from Google Cloud Console.
Only read-only scopes are requested (`https://www.googleapis.com/auth/gmail.readonly`).
On first run, `scripts/fetch_gmail_data.py` opens the OAuth browser flow and saves `token.json` locally.

### Mode 3 — Exported Mailbox (Offline)

Used when neither MCP nor credentials are available. Pass a previously exported JSON, CSV, or MBOX file.
`fetch_gmail_data.py` is skipped; only `filter_messages.py` and the analyzers run.

### Mode Selection Summary

| Condition | Mode Used |
|-----------|-----------|
| MCP Gmail tools active | Mode 1 — MCP (preferred) |
| `credentials.json` present, no MCP | Mode 2 — Python OAuth |
| Exported file provided, no MCP/credentials | Mode 3 — Offline |

> All commands work in all three modes. Mode 1 is the default and requires no setup beyond the existing MCP connection.

---

## Data Scope Definitions

Understanding what is included in each analysis scope prevents misreading report totals.

| Scope | Gmail Query | What Is Included | What Is Excluded |
|-------|-------------|------------------|------------------|
| **Inbox (default)** | `in:inbox` | Messages in the INBOX label | Sent, Drafts, Trash, Spam, archived |
| **All visible** | no label filter | INBOX + Sent + Drafts + Trash + archived | Spam (unless `--include-spam`) |
| **Spam included** (`--include-spam`) | `in:inbox OR in:spam` | Everything above + SPAM label | Nothing blocked |
| **Unread only** (`--unread-only`) | `is:unread` | Only unread messages in scope | Read messages; note: unread can be old backlog, not just today's mail |
| **Read only** (`--read-only`) | `is:read` | Only read messages in scope | Unread messages |

### Threads vs Messages

- `fetch_gmail_data.py` retrieves and counts **individual messages** by default. One email thread with 5 replies = 5 messages.
- `response_time_analyzer.py` groups by **thread ID** to pair received messages with sent replies and calculate latency.
- Report totals reflect message count unless explicitly stated as thread count.

### Why `--include-spam` Changes Totals

Spam is excluded from the INBOX query by Gmail's API. Adding `--include-spam` can increase volume counts significantly and distort sender concentration and noise ratios. Always note in reports when spam was included.

---

## Quick Start Examples

```
# Full report for today
/gmail report today

# Weekly summary
/gmail summary week

# Unread emails this month
/gmail unread month

# Top senders this year
/gmail senders year

# Custom date range with filters
/gmail custom --from 2026-01-01 --to 2026-01-31 --include-spam --has-attachments

# Suggest inbox labels
/gmail organize month

# Organization report in Portuguese as PDF
/gmail organize month --pt --pdf

# Generate PDF report
/gmail report-pdf
```
