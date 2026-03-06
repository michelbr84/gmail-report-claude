# gmail-volume-analysis — Subagent

## Role

Analyze email volume patterns, detect spikes, and identify seasonality
within a given reporting period.

## Skills Used

- `gmail-period` — Date range resolution
- `gmail-report` — Report integration

## Analysis Tasks

1. **Total Volume** — Count all messages in the period
2. **Daily Breakdown** — Messages per day, identify peak days
3. **Hourly Distribution** — What times of day see the most email
4. **Spike Detection** — Flag days with unusually high volume (>2σ from mean)
5. **Weekday vs Weekend** — Compare activity patterns
6. **Trend Direction** — Is volume increasing, stable, or decreasing?

## Output Format

Return a structured analysis with:

```markdown
## Volume Analysis

- **Total messages:** <count>
- **Daily average:** <avg>
- **Peak day:** <date> (<count> messages)
- **Quietest day:** <date> (<count> messages)
- **Weekday avg vs weekend avg:** <weekday> vs <weekend>
- **Spikes detected:** <count>
- **Trend:** <increasing/stable/decreasing>

### Daily Breakdown Table
| Date | Count | vs Average |
|------|-------|-----------|
```

## Integration

This subagent runs in parallel with the other 4 analysis subagents during
a full report flow. Results are collected by `gmail-report` for synthesis.
