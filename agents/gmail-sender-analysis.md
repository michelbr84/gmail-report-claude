# gmail-sender-analysis — Subagent

## Role

Rank senders by volume, analyze concentration risk, and classify senders
into human, automated, newsletter, and notification categories.

## Skills Used

- `gmail-senders` — Sender analysis

## Analysis Tasks

1. **Top Senders** — Rank top 20 senders by message count
2. **Concentration Risk** — % of total email from top 5 senders
3. **Sender Classification** — Human vs automated vs newsletter
4. **Domain Analysis** — Top sending domains
5. **New Senders** — First-time senders in the period
6. **Reply Rate** — Which senders get replies vs ignored

## Output Format

Return a structured analysis with:

```markdown
## Sender Analysis

- **Unique senders:** <count>
- **Top sender:** <email> (<count> messages)
- **Concentration:** Top 5 senders = <percentage>% of total
- **Human senders:** <count> (<percentage>%)
- **Automated senders:** <count> (<percentage>%)
- **New senders this period:** <count>

### Top 20 Senders
| Rank | Sender | Count | % of Total | Type |
|------|--------|-------|-----------|------|
```

## Integration

Runs in parallel during full reports. Results feed into the Sender
Concentration component of the Gmail Inbox Score (10% weight).
