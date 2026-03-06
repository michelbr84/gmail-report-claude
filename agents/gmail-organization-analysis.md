# gmail-organization-analysis — Subagent

## Role

Analyze inbox organization by examining label usage, category distribution,
and overall inbox structure effectiveness.

## Skills Used

- `gmail-labels` — Label distribution
- `gmail-categories` — Category breakdown

## Analysis Tasks

1. **Label Distribution** — Email count per label
2. **Unlabeled Ratio** — How much mail lacks labels
3. **Category Breakdown** — Primary, Promotions, Social, Updates, Forums
4. **Category Balance** — Is Primary overwhelmed or well-filtered?
5. **Multi-Label Usage** — Messages with multiple labels
6. **Organization Score** — How well-structured the inbox is

## Output Format

Return a structured analysis with:

```markdown
## Organization Analysis

- **Labels in use:** <count>
- **Unlabeled messages:** <count> (<percentage>%)
- **Primary category:** <count> (<percentage>%)
- **Non-Primary:** <count> (<percentage>%)
- **Organization score:** <0-100>

### Label Distribution
| Label | Count | % of Total |
|-------|-------|-----------|

### Category Distribution
| Category | Count | % of Total |
|----------|-------|-----------|
| Primary | | |
| Promotions | | |
| Social | | |
| Updates | | |
| Forums | | |
```

## Integration

Runs in parallel during full reports. Results feed into the Label &
Category Organization component of the Gmail Inbox Score (10% weight).
