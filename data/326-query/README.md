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
- **Judging:** LLM judge (`gpt-4o-mini`, temperature 0, deterministic rubric) — **not human-reviewed**
  for the main evaluation; a lightweight human spot-check exists separately (see below).

## Files

| File | Rows | Description |
|---|---|---|
| `queries.csv` | 326 | The query bank with stable IDs (`V001`-`V326`), language, scenario, category. |
| `evaluations.csv` | 652 | Two evaluation runs stacked (`run_variant` column): production baseline and candidate branch. |
| `human_spot_check.csv` | 326 | A single reviewer's verdict against the candidate run's automated label (314 of 326 completed). |
| `schema.json` | — | Field-level schema for all three CSVs. |
| `provenance.json` | — | Source file paths, hashes, and transformation notes. |

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

## Human spot-check

`human_spot_check.csv` records one reviewer's verdict for 314 of 326 queries, laid directly
against the candidate run's automated label for disagreement-spotting. It is **not** a full
independent re-evaluation (no result counts or top-result evidence of its own), and 12 rows are
blank (not yet reviewed). Values are preserved exactly as recorded, including non-standard
uncertainty markers (`PASS?`, `PASS？`, `PARTIAL?`).

## Known limitations

- **Not cross-platform.** No Pinterest/Bing/Google/Canva evaluation exists for these 326 queries.
- **Not human-reviewed for the main evaluation.** `relevance_label`/`relevance_score` are LLM-judge
  output. The human layer is a partial, lightweight spot-check only.
- **Candidate branch was not production-approved** at time of capture — read as a regression
  snapshot, not a current-state claim.

## Intended use

Reproducible reference for comparing two Curify search-relevance code states over a fixed,
balanced (language x scenario) query bank, and for studying where an LLM judge and a human spot-check
agree or disagree.

## Out-of-scope use

Do not use this dataset to claim a cross-platform ranking of Curify vs. other platforms. Do not
present the candidate run as representative of current production Curify search.

## Loading example

```python
import pandas as pd
queries = pd.read_csv("data/326-query/queries.csv")
evals = pd.read_csv("data/326-query/evaluations.csv")
human = pd.read_csv("data/326-query/human_spot_check.csv")

# PASS/PARTIAL/FAIL/UNJUDGABLE distribution per run:
evals.groupby("run_variant")["relevance_label"].value_counts()
```

## Citation and versioning

See the repository root [`CITATION.cff`](../../CITATION.cff). This is public version `1.0.0` of
this dataset (see `provenance.json`).
