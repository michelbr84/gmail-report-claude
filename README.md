<p align="center">
  <img src="assets/banner.png" alt="Gmail Reports Claude Code Skill Suite" width="900"/>
</p>

<p align="center">
  <strong>Gmail-first, reporting-powered.</strong> Analyze inbox activity by day, week, month, year, or custom range<br/>
  with flexible filters for unread messages, spam inclusion, labels, categories, senders, attachments, and response behavior.
</p>

<p align="center">
  Turn raw Gmail data into clear, client-ready or personal productivity reports.
</p>

---

## Why This Exists

Most inbox tools show activity. This skill suite explains it.

Instead of only counting emails, it helps you answer questions like:

- How many emails arrived today, this week, this month, or this year?
- How many are unread versus processed?
- Should spam be included or excluded from the report?
- Who are the top senders in a given period?
- Which labels, categories, or threads dominate the inbox?
- How much of the inbox is noise versus actionable communication?
- Are response times improving or getting worse?
- Which days or months had the highest email load?

This makes the project useful for personal productivity, executive assistance, founders, operations teams, support managers, and agencies offering Gmail reporting services.

---

## Quick Start

### One-Command Install (macOS/Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/michelbr84/gmail-report-claude/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/michelbr84/gmail-report-claude.git
cd gmail-report-claude
./install.sh
```

### Requirements

- Python 3.8+
- Claude Code CLI
- Git
- Gmail account
- Gmail API access or OAuth credentials
- Optional: exported mailbox data in JSON/CSV/MBOX for offline analysis

---

## Commands

Open Claude Code and use these commands:

| Command | What It Does |
|---------|-------------|
| `/gmail report today` | Full report for today’s emails |
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
| `/gmail custom --from 2026-03-01 --to 2026-03-06` | Custom date range report |
| `/gmail custom --from 2026-03-01 --to 2026-03-06 --unread-only` | Custom report for unread only |
| `/gmail custom --from 2026-03-01 --to 2026-03-06 --include-spam` | Custom report with Spam included |
| `/gmail custom --from 2026-03-01 --to 2026-03-06 --all-received` | Include all received emails in the period |
| `/gmail report-pdf` | Generate a professional PDF report with charts and tables |

### Common Filters

Supported filters can be mixed depending on the skill:

- `--today`
- `--week`
- `--month`
- `--year`
- `--from YYYY-MM-DD`
- `--to YYYY-MM-DD`
- `--include-spam`
- `--exclude-spam`
- `--unread-only`
- `--read-only`
- `--all-received`
- `--label "Work"`
- `--category promotions`
- `--sender someone@example.com`
- `--has-attachments`

---

## Architecture

```
gmail-report-claude/
├── gmail/                             # Main skill orchestrator
│   └── SKILL.md                       # Primary skill file with commands & routing
├── skills/                            # Specialized sub-skills
│   ├── gmail-report/                  # Full report orchestration & scoring
│   ├── gmail-summary/                 # Quick inbox summary
│   ├── gmail-period/                  # Day/week/month/year/custom range handling
│   ├── gmail-unread/                  # Unread-only filtering and analysis
│   ├── gmail-spam/                    # Spam inclusion/exclusion analysis
│   ├── gmail-senders/                 # Top senders and sender concentration
│   ├── gmail-labels/                  # Label distribution analysis
│   ├── gmail-categories/              # Promotions/Social/Primary/etc. analysis
│   ├── gmail-attachments/             # Attachment volume and file pattern analysis
│   ├── gmail-response-time/           # Reply speed and follow-up behavior
│   ├── gmail-trends/                  # Trend lines across days, weeks, and months
│   ├── gmail-custom/                  # Custom date-range reports with mixed filters
│   ├── gmail-report-md/               # Markdown report generation
│   └── gmail-report-pdf/              # Professional PDF report with charts
├── agents/                            # Parallel subagents
│   ├── gmail-volume-analysis.md       # Volume, spikes, seasonality
│   ├── gmail-noise-analysis.md        # Spam, low-value mail, clutter patterns
│   ├── gmail-sender-analysis.md       # Sender ranking and concentration analysis
│   ├── gmail-organization-analysis.md # Labels, categories, and inbox structure
│   └── gmail-response-analysis.md     # Response behavior and follow-up patterns
├── scripts/                           # Python utilities
│   ├── fetch_gmail_data.py            # Gmail API retrieval and normalization
│   ├── filter_messages.py             # Date, spam, unread, and label filtering
│   ├── sender_ranker.py               # Sender aggregation and ranking
│   ├── trend_analyzer.py              # Time-series analysis
│   ├── response_time_analyzer.py      # Reply latency estimation
│   └── generate_pdf_report.py         # PDF report generator
├── templates/                         # Report templates
│   ├── summary.md                     # Executive summary template
│   ├── monthly-report.md              # Monthly report template
│   ├── yearly-report.md               # Yearly report template
│   └── custom-report.md               # Custom date range template
├── install.sh                         # One-command installer
├── uninstall.sh                       # Uninstaller
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## How It Works

### Full Report Flow

When you run a command like `/gmail report month`:

1. **Data Collection** — Authenticates with Gmail and fetches messages for the requested period
2. **Filtering** — Applies the selected options such as unread-only, include-spam, sender, label, category, or attachments
3. **Parallel Analysis** — Launches focused analyzers simultaneously:
   - Volume Analysis
   - Noise and Spam Analysis
   - Sender Analysis
   - Label and Category Analysis
   - Response Behavior Analysis
4. **Synthesis** — Aggregates findings into a composite Gmail Inbox Score (0-100)
5. **Report** — Produces a markdown or PDF report with charts, tables, priorities, and plain-language conclusions

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

This score is designed to make reports easier to compare across time periods.

Example:

- A daily report can be compared against the weekly average
- A monthly report can be compared against the previous month
- A yearly report can surface the heaviest communication periods

---

## Key Features

### Flexible Time Windows
Analyze Gmail activity by:

- Day
- Week
- Month
- Year
- Custom date range

### Spam Inclusion Control
Choose whether Spam is part of the report or excluded from the analysis. This is useful when measuring real inbox workload versus total incoming email noise.

### Unread-Only or All Received
Generate reports focused only on unread emails, only read emails, or all received messages in the selected period.

### Sender Intelligence
Identify:

- Top senders
- Repeat senders
- Sender concentration risk
- High-noise senders
- Important contacts versus clutter sources

### Label and Category Breakdown
Measure how email is distributed across:

- Custom Gmail labels
- Inbox categories such as Primary, Promotions, Social, Updates, and Forums

### Attachment Insights
Report on attachment-heavy activity, large-file patterns, and periods with unusually high file traffic.

### Response-Time Insights
Estimate:

- Average reply latency
- Fastest and slowest response windows
- Conversations likely needing follow-up
- Whether backlog is getting healthier or worse

### Client-Ready Reports
Generate professional reports in markdown or PDF format with:

- Executive summary
- KPI tables
- Trend charts
- Top senders tables
- Spam vs non-spam comparison
- Unread backlog summary
- Recommendations and next actions

---

## Example Report Questions

This skill suite is designed to answer prompts like:

- “How many emails did I receive today?”
- “Give me a report of this week’s unread emails.”
- “Show all emails received this month including Spam.”
- “Which senders emailed me most this year?”
- “How much of my inbox last month was Promotions versus Primary?”
- “Create a PDF report for my Gmail activity from January 1 to January 31.”
- “Compare this week’s volume against last week.”
- “Tell me whether my unread backlog is increasing month over month.”

---

## Use Cases

- **Personal Productivity** — Understand overload, unread backlog, and email habits
- **Executive Assistants** — Prepare inbox summaries for leaders
- **Founders & Operators** — Measure communication load by period
- **Support Teams** — Track response behavior and email pressure
- **Sales Teams** — Analyze sender activity and follow-up consistency
- **Recruiters** — Review candidate email volume and reply cadence
- **Agencies** — Deliver Gmail reporting as a service to clients

---

## Output Formats

### Markdown Report
Ideal for Claude Code output, documentation, internal notes, and quick sharing.

### PDF Report
Ideal for client delivery, recurring monthly reviews, executive summaries, and archive-friendly reporting.

Typical PDF sections:

- Cover page
- Period analyzed
- Filters used
- Key metrics
- Charts
- Top senders
- Label/category breakdown
- Spam vs inbox comparison
- Recommendations

---

## Privacy & Data Handling

This project should be implemented to analyze only the data the user explicitly authorizes.

Recommended modes:

- Direct Gmail API access via OAuth
- Read-only Gmail scopes whenever possible
- Offline analysis from exported mailbox files
- Optional anonymization of sender addresses in generated reports

Do not request broader mailbox permissions than necessary for the selected report.

---

## Uninstall

```bash
./uninstall.sh
```

Or manually:

```bash
rm -rf ~/.claude/skills/gmail ~/.claude/skills/gmail-* ~/.claude/agents/gmail-*.md
```

---

## Service / Business Angle

This project can also be positioned as a Gmail reporting service.

Possible offers:

- Weekly inbox health report
- Monthly executive Gmail summary
- Spam and clutter audit
- Unread backlog cleanup report
- Team response-time analysis
- Custom date-range reporting for legal, finance, operations, or recruiting workflows

This turns the skill suite into both a productivity tool and a service product.

---

## License

MIT License

---

## Contributing

Contributions welcome. Suggested areas:

- Gmail API integrations
- Better thread analysis
- Improved response-time inference
- More filters and report templates
- Better PDF visualizations
- Privacy-preserving reporting modes

---

Built for Gmail reporting workflows.# gmail-report-claude
