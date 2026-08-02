# 326-query benchmark

A curated regression benchmark evaluating two states of Curify's own search-relevance pipeline
(a production baseline and a candidate branch) over a fixed bank of 326 "Easy Query" terms.
Internal evaluation converted for public release. See [`../../METHODOLOGY.md`](../../METHODOLOGY.md)
for full methodology and [`../../SOURCE_AUDIT.md`](../../SOURCE_AUDIT.md) for source provenance.

## At a glance

- **Queries:** 326 (163 Chinese / 163 English), across 4 scenarios: creative/merch (82),
  brand/business (82), marketing/e-commerce (82), education (80)
- **Systems evaluated:** Curify only — production baseline vs. a candidate branch (see below).
  **Not** a cross-platform comparison.
- **Query-bank date:** 2026-07-16. **Evaluation dates:** 2026-07-21 (baseline), 2026-07-22 (candidate).
- **Judging:** LLM judge (`gpt-4o-mini`, temperature 0, deterministic rubric) — **not human-reviewed**.
  Human-review data is not included in this public release.

## Files

| File | Rows | Description |
|---|---|---|
| `queries.csv` | 326 | The query bank with stable IDs (`V001`-`V326`), language, scenario, category. |
| `evaluations.csv` | 652 | Two evaluation runs stacked (`run_variant` column): production baseline and candidate branch. |
| `schema.json` | — | Field-level schema for both CSVs. |
| `provenance.json` | — | Source file paths, hashes, and transformation notes. |
| `google-images/` | 326 screenshots | Real Google Images search-results screenshot evidence, one per query. See [`google-images/README.md`](google-images/README.md). |
| `curify/` | 326 screenshots | Real Curify search-results screenshot evidence, one per query. See [`curify/README.md`](curify/README.md). |

## Systems evaluated (`run_variant` in `evaluations.csv`)

- `production_baseline_2026-07-21` — Curify production `main`, captured 2026-07-21.
- `candidate_2026-07-22_0e794cd9` — a candidate branch capturing a specific search-relevance fix,
  captured 2026-07-22. This candidate's own internal report concluded it was **not yet approved**
  to replace production at the time of capture — treat this as a regression-testing snapshot, not
  a claim about current production quality.

Full commit SHAs are in `provenance.json` / `METHODOLOGY.md`.

## Label definitions (`relevance_label`)

`PASS`, `PARTIAL`, `FAIL`, `UNJUDGABLE` — see [`../../METHODOLOGY.md`](../../METHODOLOGY.md) for the
exact rubric (result-rate thresholds, semantic-drift and intent-preservation conditions).

| run_variant | PASS | PARTIAL | FAIL | UNJUDGABLE |
|---|---|---|---|---|
| production_baseline_2026-07-21 | 24 | 83 | 207 | 12 |
| candidate_2026-07-22_0e794cd9 | 38 | 86 | 195 | 7 |

`zero_result` / `low_result` counts (result-count thresholds, defined in METHODOLOGY.md):

| run_variant | zero_result | low_result |
|---|---|---|
| production_baseline_2026-07-21 | 23 | 19 |
| candidate_2026-07-22_0e794cd9 | 20 | 18 |

## Screenshot evidence (326/326 Google Images, 326/326 Curify)

As of this update, real, unedited search-results screenshots exist for **all 326 queries** on two
search surfaces:

- **Google Images** — [`google-images/`](google-images/README.md), 326/326, captured 2026-08-01/02.
- **Curify** (`curify-ai.com`) — [`curify/`](curify/README.md), 326/326, captured 2026-08-02/03. 319
  are standard `/search?q=...` results pages; 7 are Curify's own deterministic client-side redirect
  to a `/topics/...` category page for certain single generic words (e.g. "logo", "map") — captured
  as real evidence of that actual product behavior, not worked around. See `curify/README.md` for
  the full list and how each is marked.

**This is screenshot evidence, not a new evaluation.** No relevance judgment, score, or ranking was
generated for either platform — `evaluations.csv` still scores Curify only (production baseline vs.
candidate branch, as below) and was not changed or re-run for this update. Do not read the presence
of Google Images screenshots as a cross-platform relevance comparison; no such comparison exists in
this release.

## Known limitations

- **Not a scored cross-platform comparison.** Real screenshots now exist for Google Images and
  Curify (see above), but no relevance judgment, ranking, or score was generated for Google Images,
  and the existing Curify `evaluations.csv` scores were not re-generated from these screenshots. No
  Pinterest/Bing/Canva evidence of any kind exists for these 326 queries.
- **Not human-reviewed.** `relevance_label`/`relevance_score` are LLM-judge output.
  Human-review data is not included in this public release.
- **Candidate branch was not production-approved** at time of capture — read as a regression
  snapshot, not a current-state claim.
- **Screenshot evidence is a later, separate point-in-time capture** (2026-08-01 to 2026-08-03) than
  the `evaluations.csv` runs (2026-07-21/22) — the two should not be conflated as the same snapshot.

## Intended use

Reproducible reference for comparing two Curify search-relevance code states over a fixed,
balanced (language x scenario) query bank.

## Out-of-scope use

Do not use this dataset to claim a cross-platform ranking of Curify vs. other platforms. Do not
present the candidate run as representative of current production Curify search. Do not present
`relevance_label`/`relevance_score` as human-reviewed ground truth. Do not present the Google
Images / Curify screenshot evidence (`google-images/`, `curify/`) as a scored or ranked comparison —
it is unscored visual evidence of what each surface actually returned at capture time, nothing more.

## Loading example

```python
import pandas as pd
queries = pd.read_csv("data/326-query/queries.csv")
evals = pd.read_csv("data/326-query/evaluations.csv")

# PASS/PARTIAL/FAIL/UNJUDGABLE distribution per run:
evals.groupby("run_variant")["relevance_label"].value_counts()
```

## Citation and versioning

See the repository root [`CITATION.cff`](../../CITATION.cff). This is public version `1.0.0` of
this dataset (see `provenance.json`).
