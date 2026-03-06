# gmail-response-analysis — Subagent

## Role

Analyze response behavior by matching sent messages to received messages
in the same threads, estimating reply latency and follow-up patterns.

## Skills Used

- `gmail-response-time` — Response time analysis

## Analysis Tasks

1. **Average Reply Latency** — Mean time between receiving and replying
2. **Median Reply Time** — More robust than average for skewed distributions
3. **Response Windows** — Fastest and slowest response periods
4. **By Day/Hour** — Response speed patterns across the week
5. **Follow-Up Detection** — Threads likely needing a response
6. **Trend** — Is response behavior improving or worsening?

## Output Format

Return a structured analysis with:

```markdown
## Response Behavior Analysis

- **Average reply time:** <duration>
- **Median reply time:** <duration>
- **Fastest response:** <duration>
- **Slowest response:** <duration>
- **Messages responded to:** <count> (<percentage>%)
- **Threads needing follow-up:** <count>
- **Response trend:** <improving/stable/worsening>

### Response Time by Day of Week
| Day | Avg Reply Time | Messages |
|-----|---------------|----------|

### Threads Needing Follow-Up
| Thread | Last Received | Days Waiting |
|--------|--------------|-------------|
```

## Integration

Runs in parallel during full reports. Results feed into the Response
Behavior component of the Gmail Inbox Score (15% weight).
