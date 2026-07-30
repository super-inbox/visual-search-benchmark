# Methodology

This repository publishes two internal Curify evaluation datasets. **They are not the same kind of
benchmark** — different query sets, different systems under test, different judging methodology.
Read this document before comparing numbers across the two folders.

## 68-query benchmark (`data/68-query/`)

**What it measures:** how Curify's own search (`curify-ai.com/search`) performs against 68
hand-curated "gold" queries, spanning four scenes (brand, marketing/e-commerce, education,
cultural-creative).

**What it does NOT measure:** it is not a full cross-platform comparison. Only Curify was evaluated
with structured, per-query relevance data across all 68 queries. A separate, smaller pilot captured
real cross-platform screenshots (Curify/Bing/Google/Canva/Pinterest) for **12 of the 68** queries —
those 62 images (5 platforms x 12 queries, plus 2 backup captures) **are published** in
`data/68-query/images/`, with a browsable offline gallery at `data/68-query/gallery/index.html`.
The pilot produced free-text AI-generated visual observations for the competitor platforms, not
numeric scores, and only Curify's screenshot carries a formal PASS/WARN/FAIL-style label
(`visual_curify_label`, cross-checked against `claude_relevance_label`). See
`docs/68_IMAGE_SOURCE_INVENTORY.md` and `data/68-query/IMAGE_MAPPING_REPORT.md` for exactly what is
and isn't covered — the other 56 of 68 queries have no image evidence anywhere in the source data.

**Collection process:**
1. 68 queries were curated from a larger candidate pool (a 58-query seed set expanded to
   roughly 1,100 candidates across four generation tracks, then filtered to a P0/"keep" pool and
   hand-selected down to 68 — see `SOURCE_AUDIT.md` for the exact lineage).
2. Each query was run against Curify's live search via browser automation (Playwright), capturing
   the rendered result titles, tags, types, and any "no results" / "showing broadened results"
   messaging.
3. An LLM (Claude) read each automated-collection row and produced a first-pass relevance label.

**Label definitions (`automated_relevance_labels.csv`, `claude_relevance_label`):**
- `PASS` — results match query intent (0 occurrences in this snapshot).
- `WARN` — results partially match or show a milder issue (25 occurrences).
- `FAIL` — results do not match query intent, or query was broadened away from its meaning, or
  zero relevant results (43 occurrences).

**Human review status:** a manual-review spreadsheet and rubric (PASS/WARN/FAIL/UNCLEAR) were
prepared for a human pass over all 68 queries. **No human reviewer ever completed this pass** —
every `human_*` field in the source file was empty as of the source date and remains empty; those
columns were dropped from the public release rather than published as blank placeholders (see
`data/68-query/provenance.json`).

**No diversity or actionability dimension** exists in the source data for this benchmark, despite
earlier internal planning documents proposing one. Only a single relevance dimension was ever
actually collected.

## 326-query benchmark (`data/326-query/`)

**What it measures:** a regression comparison of Curify's own internal search-relevance pipeline
across two code states — a production baseline and a candidate branch — over a fixed bank of 326
"Easy Query" terms (163 Chinese / 163 English, split across four scenarios: creative/merch,
brand/business, marketing/e-commerce, education).

**What it does NOT measure:** it is not a cross-platform comparison. No Pinterest/Bing/Google/Canva
evaluation exists anywhere in the source material for these 326 queries.

**Systems under test (`run_variant` in `evaluations.csv`):**
- `production_baseline_2026-07-21` — Curify production `main`, commit `c550856e07c2c7058f955799beb9738e7a9b4f0a`, captured 2026-07-21.
- `candidate_2026-07-22_0e794cd9` — branch `baobao/search-relevance-prod-main-v2-r3-root-cause-fix-2026-07-19`,
  commit `0e794cd91396a96cd56fd1d8f7f1495909f3adc5`, captured 2026-07-22 ("Cluster A/B latest fix" run).
  This candidate's own internal report explicitly concluded `NEEDS_MORE_FIXES` / not yet approved
  to replace production at the time of capture.

**Collection process:** for each query and each run variant, a real HTTP request was made to a
locally-running `next start` build of the relevant commit, and the search response (result counts,
top-5 titles) was captured. This is real search-engine output, not a synthetic re-implementation.

**Judging process:** an LLM judge (`gpt-4o-mini`, temperature 0, deterministic rubric
`rubric-v1.1`) scored the top-5 results per query:
- `PASS` — `irrelevant_rate <= 0.20` AND intent preserved AND drift not severe AND
  (`relevant_rate >= 0.60` OR (`relevant+partial_rate >= 0.80` AND `relevant_rate >= 0.20`)).
- `FAIL` — `irrelevant_rate > 0.60`, OR severe semantic drift with intent not preserved, OR
  zero results (auto-FAIL).
- `PARTIAL` — has judgeable results, not a hard-fail, not PASS.
- `UNJUDGABLE` — no top-5 item had usable evidence, the judge call failed after retries, or there
  were zero judgeable labels.
- `zero_result` — `total_results === 0`. `low_result` — `0 < total_results < 5`.

**Human review status:** an internal human-verification pass exists over this query set, separate
from the LLM-judge evaluation above. **It is not included in this public release** — no human
verdicts, counts, or related file are published here. `relevance_label`/`relevance_score` in
`evaluations.csv` are LLM-judge output only.

## Why the two benchmarks are not merged

The 68-query and 326-query datasets differ in query set, system(s) compared, label vocabulary
(`PASS/WARN/FAIL` vs. `PASS/PARTIAL/FAIL/UNJUDGABLE`), and judging method (single LLM pass vs.
production-vs-candidate LLM-judge regression). Forcing them into one shared schema would misrepresent
both. Each benchmark's `schema.json` documents its actual fields; `data/README.md` and the folder
READMEs point out the differences relevant to interpreting each one.
