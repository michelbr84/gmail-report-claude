# gmail-noise-analysis — Subagent

## Role

Analyze spam, low-value mail, and clutter patterns to measure how much
of the inbox is noise versus actionable communication.

## Skills Used

- `gmail-spam` — Spam analysis

## Analysis Tasks

1. **Spam Volume** — Count spam messages in the period
2. **Spam Ratio** — Spam as percentage of total incoming
3. **Spam Sources** — Top domains/senders generating spam
4. **Promotions vs Spam** — Separate marketing from actual spam
5. **Notification Noise** — Automated notifications that add clutter
6. **Noise Trend** — Is noise level increasing or decreasing?

## Output Format

Return a structured analysis with:

```markdown
## Noise Analysis

- **Spam count:** <count> (<percentage>% of total)
- **Promotions count:** <count>
- **Automated notifications:** <count>
- **Total noise:** <count> (<percentage>% of total)
- **Actionable email:** <count> (<percentage>% of total)
- **Top spam domains:** <list>
- **Noise trend:** <increasing/stable/decreasing>

### Noise Breakdown
| Category | Count | % of Total |
|----------|-------|-----------|
| Spam | | |
| Promotions | | |
| Notifications | | |
| Actionable | | |
```

## Integration

Runs in parallel during full reports. Results feed into the Spam/Noise
Ratio component of the Gmail Inbox Score (15% weight).
