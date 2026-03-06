# gmail-organization-analysis — Subagent

## Role

Analyze inbox organization: descriptive label and category distribution
**plus** prescriptive organization advice (label taxonomy suggestions,
Gmail filter recommendations, and organization score).

## Skills Used

- `gmail-labels` — Label distribution (descriptive: what exists today)
- `gmail-categories` — Category breakdown (Primary, Social, Promotions…)
- `gmail-organize` — Inbox organization advisor (prescriptive: what should exist)

## Analysis Tasks

### Descriptive Analysis
1. **Label Distribution** — Email count per label
2. **Unlabeled Ratio** — How much mail lacks custom labels
3. **Category Breakdown** — Primary, Promotions, Social, Updates, Forums
4. **Category Balance** — Is Primary overwhelmed or well-filtered?
5. **Multi-Label Usage** — Messages with multiple labels

### Prescriptive Analysis
6. **Cluster Detection** — Group unlabeled emails by sender, domain, subject, and content type
7. **Label Taxonomy** — Suggest new labels based on detected clusters
8. **Filter Rules** — Suggest Gmail filters to auto-apply labels going forward
9. **Organization Score** — Composite 0-100 score combining current labeling and cluster coverage

## Scripts Used

- `scripts/organization_analyzer.py` — Inbox clustering, label suggestion, and scoring
  - Supports `--lang pt` for Portuguese output
  - Supports `--examples N` to control sample size per cluster

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

### Suggested Labels
| Label | Rationale | Volume | Confidence |
|-------|-----------|--------|------------|

### Suggested Gmail Filters
| Criteria | Action | Target Label |
|----------|--------|--------------|
```

## Integration

Runs in parallel during full reports. Results feed into the Label &
Category Organization component of the Gmail Inbox Score (10% weight).

When invoked standalone via `/gmail organize`, produces a full organization
report with taxonomy, examples, filter suggestions, and an organization
score using `templates/organization-report.md`.
