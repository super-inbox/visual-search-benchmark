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
| `results.jsonl` | 62 | Cross-platform image evidence records (12 of the 68 queries only — see below). |
| `image_manifest.json` | — | Per-file inventory: hashes, dimensions, decode status, duplicates. |
| `IMAGE_MAPPING_REPORT.md` | — | Confirmed/probable/unknown mapping breakdown for the image evidence. |
| `images/<platform>/` | 62 files | The actual screenshot evidence (Curify, Bing, Google, Canva, Pinterest). |
| `gallery/index.html` | — | Offline, filterable image gallery — open directly in a browser, no server needed. |

## Image evidence (12 of 68 queries)

Real, unedited cross-platform screenshots exist for **12 of the 68** queries —
`q002, q006, q009, q010, q015, q016, q034, q046, q053, q060, q064, q068` — captured 2026-07-07/09
across Curify, Bing Images, Google Images, Canva, and Pinterest. **The other 56 queries have no
image evidence**; this is a limit of the source data, not a curation choice, and it is not padded
out or approximated.

Every image is a full-page SERP screenshot (not a single cropped result), so `organic_rank` is
`null`/UNKNOWN for all 62 records by design. Only the Curify screenshot in each query carries a
formal label (`FAIL` for all 12, matching the already-published `claude_relevance_label`); the four
competitor screenshots carry free-text observations only (no numeric score), reflecting what the
source data actually contains.

Browse it at [`gallery/index.html`](gallery/index.html) (works offline, double-click to open — see
the repo-root [gallery README](../../docs/68_IMAGE_SOURCE_INVENTORY.md) for methodology and
[`IMAGE_MAPPING_REPORT.md`](IMAGE_MAPPING_REPORT.md) for the full mapping-confidence breakdown).
See also [`../../docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md`](../../docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md)
for a curated walkthrough of a few of these cases, and
[`../../docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md`](../../docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md)
for the licensing/rights status of the third-party screenshots (they are **not** CC BY 4.0 — the
underlying platform content remains the property of its respective rights holders).

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

- **Cross-platform evidence covers 12 of 68 queries, not all 68.** Only Curify has structured
  per-query relevance data for the full 68. A separate pilot captured real screenshots across
  Curify/Bing/Google/Canva/Pinterest for 12 of the 68 queries (published in `images/` — see above),
  but as AI-generated visual descriptions for the competitor platforms (no numeric score), not a
  formal cross-platform ranking benchmark. Do not extrapolate the 12-query pattern to the other 56.
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

Do not use this dataset to claim a cross-platform *ranking* of Curify vs. other search/design
platforms — no scored comparison exists in this data, on any of the 68 queries. The 12-query image
evidence is qualitative (screenshots + free-text observations), not a scored benchmark, and covers
only 12 of 68 queries — do not generalize it to the full set. Do not present `claude_relevance_label`
(or the screenshot-level `visual_curify_label`) as a human-reviewed ground truth. Do not present the
third-party (Bing/Google/Canva/Pinterest) screenshots as Curify-owned or freely-licensed content —
see `../../docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md`.

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
