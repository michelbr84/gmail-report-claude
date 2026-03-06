---
name: gmail-organize
description: >
  Inbox organization advisor. Detects unlabeled emails, clusters them by
  sender, domain, subject pattern, and content type, then suggests a complete
  label taxonomy with Gmail filter rules. Prescriptive counterpart to
  gmail-labels (which is descriptive). Supports --pdf and --pt (Portuguese).
---

# gmail-organize — Inbox Organization Advisor

## Purpose

Analyze emails that lack useful labels and suggest a complete, actionable
label taxonomy with Gmail filter rules. While `gmail-labels` answers
**"how is your inbox organized today"**, this skill answers
**"how should your inbox be organized"**.

## Trigger

- `/gmail organize month`
- `/gmail organize week`
- `/gmail organize year`
- `/gmail organize --from 2026-02-01 --to 2026-03-01`
- `/gmail suggest-labels month` (alias)

## Supported Flags

All standard period and filter flags apply, plus:

- `--pdf` — Generate PDF version of the organization report
- `--pt` — Output report in Portuguese (default: English)
- `--include-spam` — Include spam when analyzing clutter patterns
- `--unread-only` — Focus on unread backlog organization

## What It Analyzes

1. **Unlabeled emails** — Messages with only `INBOX` or `CATEGORY_*` labels
2. **Sender patterns** — Frequent senders, domains, automated origins
3. **Subject patterns** — Recurring keywords, prefixes, formats
4. **Content type** — Newsletters, receipts, notifications, human conversation
5. **Domain clusters** — Groups by sender domain (e.g., all `@github.com`)
6. **Repetitive messages** — Same sender + similar subject = pattern

## Clustering Strategy

The analyzer identifies natural groupings and maps them to label suggestions:

| Pattern Detected | Suggested Label | Confidence |
|-----------------|----------------|------------|
| Recurring newsletter sender | `Newsletters` | High |
| Payment/receipt subjects | `Receipts` | High |
| Bank/financial domains | `Finance` | High |
| Travel booking confirmations | `Travel` | Medium |
| Work-related domains | `Work` | Medium |
| Family member addresses | `Family` | Medium |
| AI tool notifications | `AI Tools` | Medium |
| Security alerts/2FA | `Security` | High |
| Shopping/order confirmations | `Shopping` | High |
| Service notifications | `Notifications` | High |
| Subscription confirmations | `Subscriptions` | Medium |
| Unanswered threads | `Follow Up` | Medium |

Custom clusters are generated dynamically based on actual data — not limited to these defaults.

## Workflow

1. **Fetch data** for the period
2. **Filter to unlabeled** — Keep only messages without custom labels
3. **Run `scripts/organization_analyzer.py`** to cluster and suggest
4. **Generate report** using `templates/organization-report.md`
5. Optionally generate PDF via `scripts/generate_pdf_report.py`

## Report Output

### Sections

1. **Overview**
   - Total emails analyzed
   - Unlabeled count and percentage
   - Clusters found

2. **Suggested Label Taxonomy**
   - Label name
   - Rationale
   - Estimated volume
   - Confidence (High / Medium / Low)

3. **Cluster Examples**
   - 3–5 sample emails per cluster
   - Sender, subject, date

4. **Suggested Gmail Filters**
   - Match criteria (from, subject, has:attachment, etc.)
   - Recommended action (apply label, skip inbox, etc.)
   - Target label

5. **Organization Score (0–100)**
   - Current organization level
   - Improvement opportunity

### Output Files

| Flag | Output |
|------|--------|
| (default) | `GMAIL-REPORT-ORGANIZE.md` |
| `--pdf` | `GMAIL-REPORT-ORGANIZE.pdf` |
| `--pt` | Report in Portuguese |
| `--pdf --pt` | PDF in Portuguese |

## V1 Scope (Current)

- ✅ Analysis and clustering
- ✅ Label taxonomy suggestion
- ✅ Gmail filter rules as text
- ✅ Organization score
- ✅ Markdown and PDF output
- ✅ Portuguese language support
- ❌ Automatic label application (future v2)
- ❌ Filter export to Gmail format (future v2)

## Integration

This skill uses `gmail-organization-analysis` subagent for the clustering
phase during full reports, and can also run standalone via `/gmail organize`.
