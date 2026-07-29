# Source Audit

This document records how the authoritative source files for each benchmark were identified and
verified, for anyone auditing this release. It intentionally omits local filesystem paths, internal
URLs, and any information not meant for public release; only repository-relative paths (relative to
the internal source repository, which is not itself public) and content hashes are given.

## 68-query benchmark

**Query list.** `docs/daily_report/7.7/gold_query_test_set_2026-07-07.csv` —
SHA-256 `00bd2cff0f1dee8168c366020198ed592d0f9654786ff417aa00a19ba4c7ae68`. Verified: 68 data rows,
68 unique query values, 0 duplicates, 0 empty. This hash is independently corroborated by a
separate internal engineering report that re-derived and cited the same hash.

**Lineage.** The 68 queries were selected from a larger candidate pool that itself expanded an
original 58-query seed set: seed (58) -> four parallel expansion tracks (~1,100 total candidates
across four files) -> filtered to a "P0 + keep" pool -> 68 hand-selected. The 58-query seed set is
a *different, separate* dataset (used elsewhere for an unrelated cross-platform automated pilot)
and is not itself part of this 68-query benchmark.

**Evaluation.** `docs/daily_report/7.9/curify_search_auto_collect_with_claude_relevance_2026-07-07.csv` —
SHA-256 `a1a7381927f13b6592e3bcd60eeb49c3da9642be878096b5f833083bf884d897`. 68 rows, 1:1 with the
query list by exact query-text match. Confirmed to contain: real automated Curify search-collection
data, plus an LLM (Claude)-generated relevance label. Confirmed **not** to contain any completed
human review (the `human_*` columns were checked and are 100% empty).

**Rejected/superseded alternatives:**
- A later re-run of the same 68 queries (`docs/daily_report/7.14/.../hard_queries_manual_review_68_2026-07-14.csv`)
  does have a fully-populated `human_relevance_label` column, but its own methodology note describes
  an "independent spot-check" re-review with no identifiable named human reviewer — its provenance
  as genuine human judgment (vs. an LLM self-review under a human-sounding column name) could not be
  verified, so it was not used.
- A cross-platform (Curify/Pinterest/Bing/Google/Canva) automated-collection pilot exists for a
  *different*, 58-query set. It was not used because it is a different query list, and its data is
  automated result/label counts rather than a relevance judgment.
- A 12-query cross-platform screenshot subset of the 68 exists, but only as images plus free-text
  AI-generated visual observations (no score), and at least one row's status text was found to be
  stale relative to its own accompanying notes. Not included in this release.

## 326-query benchmark

**Query list.** `docs/daily_report/7.16/easy-query-bank-v3/easy_query_bank_v2_2026-07-16.csv` —
SHA-256 `c5b1368e33ab601884ad91aff21802c64391bee781b6daa2f3ef50e4d54a08c6`. 326 rows, 0 duplicates,
0 empty, 163 Chinese / 163 English. This exact file and hash is cited as the `benchmark_input` by
every downstream evaluation run examined (2026-07-19, 2026-07-20, 2026-07-21, 2026-07-22),
making it the most externally-corroborated candidate. Stable IDs (`V001`-`V326`) were taken from a
companion file, `docs/daily_report/7.16/easy-query-v2-validation/query_input/easy_query_v2_input_with_ids.csv`
(SHA-256 `f51bd68e2139cfcca72a5235df6140b75e57c86574353ccf319645de7c13fa7a`), cross-checked row-by-row
against the query bank (0 mismatches).

**Rejected/superseded alternative:** an earlier, unrelated 328-query "legacy seed bank"
(`easy_queries_cleaned_300_plus_2026-07-14.csv`, IDs `E001`-`E328`) is explicitly disclaimed in
later internal manifests as a separate, independent set not underlying the 326-query evaluations.
It was not used.

**Evaluation runs.** Two runs were selected for the public `evaluations.csv`, matched by exact
`row_index` <-> query-ID alignment against the query bank (0 mismatches in either file):
- `docs/daily_report/7.21/scorer-v1.1-evaluation-2026-07-21/eval_raw/BASELINE_EASY326.csv` —
  SHA-256 `0b8d15173c5a86a683c5d1e84a93c13fc5fcc75b4e2ffc4e44565a6a1af3d9fa` (production baseline).
- `docs/daily_report/7.22/cluster-ab-latest-fix-full326-2026-07-22/03_FULL326_LATEST_RESULTS.csv` —
  SHA-256 `08c1b6a5e89c94066f37715d90f49e25ed19a6a017eb0e53c2c9fbdebc24c4eb` (candidate branch).

The 2026-07-22 run was preferred over four earlier candidate runs (2026-07-16, 2026-07-17,
2026-07-19, 2026-07-21) as the most recent and most rigorously self-documented: it ships its own
exact-commit config lock, a full internal SHA-256 manifest of every file in its run directory
(verified: 35 of 36 listed files match; the one mismatch is an evaluation report that was
subsequently amended by a later commit, not a data file), a per-query completeness check
confirming 326/326 coverage, and a run log ending in a clean exit. Its identifying commit
(`0e794cd91396a96cd56fd1d8f7f1495909f3adc5` on branch
`baobao/search-relevance-prod-main-v2-r3-root-cause-fix-2026-07-19`) matches a provenance
reference supplied independently by the requester of this release, providing an added
cross-check. Earlier runs (2026-07-16/17/19) evaluate the same query bank but earlier candidate
code states superseded by the 2026-07-22 fix, and were not selected.

**Label vocabulary.** Verified verbatim across every 326-query evaluation file examined:
`PASS`, `PARTIAL`, `FAIL`, `UNJUDGABLE`. `UNJUDGABLE` is a real, sometimes-nonzero value (not
invented) — confirmed nonzero in the runs selected here (12 in the baseline, 7 in the candidate).

**Human layer.** `docs/daily_report/7.23/326人工核验.xlsx` (SHA-256
`9a18b052e3b64ad4c350cd5c7c7d91c56ecf327413f0f112a5dc2751d3643fdd`) contains a genuine
single-reviewer human verdict for 314 of 326 queries, laid directly against the 2026-07-22
candidate run's automated label (confirmed: the automated-label column in this spreadsheet
reproduces the exact label distribution of the 2026-07-22 run). Included as `human_spot_check.csv`.

## Sensitive-data findings and handling

- Internal run manifests (not published) referenced local absolute filesystem paths, an internal
  preview-deployment URL, and a private GitHub repository URL. None of these appear in any file
  copied into this public release; the public `provenance.json` files use repository-relative
  paths only.
- A separate, unrelated cross-platform automated-collection pilot (the 58-query set mentioned
  above) was found to contain local absolute filesystem paths and internal dev-server loop-back
  addresses in its raw observation files. That dataset is not part of either published benchmark
  and was not copied.
- All four CSV files actually copied into this release (`gold_query_test_set`,
  `curify_search_auto_collect_with_claude_relevance`, `easy_query_bank_v2`,
  `easy_query_v2_input_with_ids`) plus the two 326-query evaluation CSVs and the human-verification
  spreadsheet were individually scanned for local paths, internal loop-back references,
  credential-shaped strings, and internal-only URLs. No genuine matches were found (one incidental
  regex hit on the substring `sk-` inside the public Curify template slug `elon-musk-tech-meme`
  was reviewed and is not a credential).
