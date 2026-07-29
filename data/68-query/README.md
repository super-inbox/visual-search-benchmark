# 68-query benchmark

A curated benchmark evaluating Curify's own visual/design search over 68 hand-selected "gold"
queries. Internal evaluation converted for public release. See [`../../METHODOLOGY.md`](../../METHODOLOGY.md)
for full methodology and [`../../SOURCE_AUDIT.md`](../../SOURCE_AUDIT.md) for source provenance.

## At a glance

- **Queries:** 68, hand-curated (English 34 / Chinese 28 / mixed 6)
- **Scenes:** brand (19), marketing/e-commerce (18), education (17), cultural-creative (14)
- **System evaluated:** Curify only (`curify-ai.com/search`)
- **Collection date:** 2026-07-07
- **Labeling:** single-pass, LLM (Claude)-generated — **not human-reviewed** (see below)
- **Dimensions scored:** relevance only (no diversity or actionability data exists for this set)

## Files

| File | Rows | Description |
|---|---|---|
| `queries.csv` | 68 | The gold query list with curation metadata (scene, priority, test-type hypothesis). |
| `automated_relevance_labels.csv` | 68 | Automated Curify search-collection output plus an LLM-generated relevance label per query. |
| `schema.json` | — | Field-level schema for both CSVs. |
| `provenance.json` | — | Source file paths, hashes, and transformation notes. |

## Column definitions

See [`schema.json`](schema.json) for the authoritative field list. Highlights:

- `queries.csv`: `query_id, query, primary_scene, secondary_scene, priority, confidence, keep_or_review, planned_test_type, ...`
- `automated_relevance_labels.csv`: `query_id, query, search_url, visible_result_count, top_10_result_titles, claude_relevance_label (PASS/WARN/FAIL), claude_issue_type, claude_confidence, ...`

## Label definitions

`claude_relevance_label`:
- `PASS` — results match query intent.
- `WARN` — results partially match, or a milder issue was detected.
- `FAIL` — results do not match query intent, the query was broadened away from its meaning, or there were effectively no relevant results.

In this snapshot: `FAIL` 43, `WARN` 25, `PASS` 0.

## Known limitations

- **Not cross-platform.** Only Curify has structured per-query evaluation data. A separate
  12-query pilot captured screenshots across Curify/Pinterest/Bing/Google/Canva, but only as
  AI-generated visual descriptions (no score), and those images are not published here.
- **Not human-reviewed.** A human-review rubric and spreadsheet were prepared, but 0 of 68 rows
  were ever completed by a human reviewer as of the source date. The `claude_relevance_label` and
  related fields are LLM-generated, single-pass judgments.
- **No diversity or actionability score.** Despite early internal planning references to these
  dimensions, no such data was ever collected for this benchmark.
- **Point-in-time snapshot.** Collected 2026-07-07; Curify's live search has likely changed since.

## Intended use

Reproducible reference for how a specific snapshot of Curify's search responded to a curated,
scenario-diverse query set, and how an LLM-based first-pass relevance judge scored it. Suitable for
tracking directional relevance regressions/improvements over time if re-run with the same queries
and judge.

## Out-of-scope use

Do not use this dataset to claim a cross-platform ranking of Curify vs. other search/design
platforms — no such comparison exists in this data. Do not present `claude_relevance_label` as a
human-reviewed ground truth.

## Loading example

```python
import pandas as pd
queries = pd.read_csv("data/68-query/queries.csv")
labels = pd.read_csv("data/68-query/automated_relevance_labels.csv")
merged = queries.merge(labels, on=["query_id", "query"])
merged["claude_relevance_label"].value_counts()
```

## Citation and versioning

See the repository root [`CITATION.cff`](../../CITATION.cff). This is public version `1.0.0` of
this dataset (see `provenance.json`).
