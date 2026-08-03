# Visual Search Benchmark

Two curated internal evaluation datasets from [Curify](https://curify-ai.com), converted for public
release: a 68-query gold set evaluating Curify's own search relevance — now including real,
browsable cross-platform screenshot evidence for 12 of the 68 queries — and a 326-query regression
benchmark comparing two states of Curify's search-relevance pipeline. This benchmark combines
real-world creative-search queries with cross-platform visual evidence (where it exists), human/LLM
relevance judgments, and query-level failure analysis — not just a query list and a final score.

> **Status:** `v1.2.0`. See [`METHODOLOGY.md`](METHODOLOGY.md) for how each benchmark was built,
> [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for source provenance and hashes, and
> [`DATASET_CARD.md`](DATASET_CARD.md) for the structured dataset-card summary.

## 1. Project overview

This repository publishes two datasets produced during Curify's own internal search-quality work:

- **68-query benchmark** — a hand-curated "gold" query set testing Curify's own visual/design
  search, with real cross-platform screenshot evidence for a 12-query subset.
- **326-query benchmark** — a broader, balanced query bank used to regression-test two states of
  Curify's search-relevance pipeline (production vs. a candidate branch).

Both were built for internal use first and converted for public release with source hashes,
provenance notes, and an explicit accounting of what is and isn't included (see `SOURCE_AUDIT.md`).

## 2. Why this benchmark exists

Most public "search quality" datasets are either query lists with no visible results, or aggregate
scores with no way to see *what actually happened*. This release instead ties together, wherever the
source data allows it: the literal query text, which platform was searched, what the platform
actually returned (as a real screenshot, not a description), and a relevance judgment — so a reader
can see a failure, not just a number. It also documents, deliberately, where that chain is
incomplete (56 of 68 queries with no image evidence; the entire 326-query set with no cross-platform
data at all) rather than smoothing that over.

## 3. What makes this dataset different

- It is not a query list alone: for the 12-query image subset, the same query is paired with real,
  unedited search-result screenshots from up to five different platforms.
- Query, platform, (where determinable) rank, image, and a relevance judgment are joined by an
  explicit, published mapping-confidence field (`confirmed` / `probable` / `unknown`) — not implied.
- It shows failures directly, with a screenshot and a stated reason, not just a pass/fail count.
- It covers real-world short queries, ambiguous intent, IP/fandom-specific terms, creative and
  stylistic requests (e.g. "low-saturation Chinese-style tea packaging," "Y2K chrome skincare
  poster"), and bilingual (Chinese/English) phrasing — the kind of query a production visual/design
  search system actually receives, not synthetic benchmark phrasing.
- It's useful beyond one company's product: for visual/creative search, multimodal retrieval,
  ranking, and recommendation research generally, and for regression testing, failure analysis, and
  retrieval evaluation specifically.

## 4. Benchmark components

| | 68-query | 326-query |
|---|---|---|
| Queries | 68, hand-curated | 326 (163 zh / 163 en) |
| System(s) evaluated | Curify only | Curify only — production baseline vs. a candidate branch |
| Cross-platform image evidence | **12 of 68 queries** (Curify/Bing/Google/Canva/Pinterest screenshots, published) | **326 of 326** (Google Images + Curify screenshots, published — unscored evidence, not a new evaluation) |
| Judging | Single-pass LLM (Claude) relevance label | LLM judge (`gpt-4o-mini`), PASS/PARTIAL/FAIL/UNJUDGABLE |
| Human review | Not included in this public release | Not included in this public release |
| Labels | `PASS` / `WARN` / `FAIL` | `PASS` / `PARTIAL` / `FAIL` / `UNJUDGABLE` |

**The two benchmarks are intentionally not merged into one schema** — different query sets,
different systems under test, different label vocabularies. See [`METHODOLOGY.md`](METHODOLOGY.md)
for why, and each dataset's own `data/*/README.md` for details.

## 5. 68-query vs. 326-query

**68-query** is the deep-evidence set: fewer queries, but for a 12-query subset you can see the
literal screenshots across five platforms plus a stated reason for each judgment. Positioning: *a
human/LLM-audited cross-platform visual search benchmark with actual ranked-page visual evidence
(where captured).*

**326-query** is the broad-coverage set: 326 queries across four scenarios in two languages, run
through two code states of the same search pipeline, for regression/coverage testing — plus real
(unscored) Google Images and Curify screenshot evidence for every one of the 326 queries.
Positioning: *a broader query-evaluation suite for testing search coverage, retrieval behavior,
relevance, and regressions, now with visible search-page evidence alongside the scored Curify
regression comparison.*

Use 68-query when you want to look at *why* something failed on a specific query. Use 326-query
when you want breadth and a production-vs-candidate regression comparison. Don't expect either to
substitute for the other — see `METHODOLOGY.md` "Why the two benchmarks are not merged."

## 6. Platforms covered

- **68-query, all 68:** Curify only (`curify-ai.com/search`).
- **68-query, 12-query image subset only:** Curify, Bing Images, Google Images, Canva, Pinterest —
  real screenshots, not simulated or described from memory.
- **326-query, scored evaluation (`evaluations.csv`):** Curify only (two code states — see
  `METHODOLOGY.md`).
- **326-query, screenshot evidence (all 326 queries):** Google Images and Curify — real,
  unscored screenshots, published in `data/326-query/google-images/` and `data/326-query/curify/`.

No platform other than Curify has structured, *scored*, per-query data anywhere in this release.
The 68-query 12-query image subset is screenshots + free-text observations for the four competitor
platforms; the 326-query Google Images / Curify screenshots are unscored visual evidence. Neither
is a scored cross-platform comparison.

## 7. Data schema

See each dataset's `schema.json` for the authoritative field list:
[`data/68-query/schema.json`](data/68-query/schema.json),
[`data/326-query/schema.json`](data/326-query/schema.json) (`queries.csv`/`evaluations.csv` only —
unchanged by the screenshot-evidence addition below). The 68-query image evidence has its own
record schema in [`data/68-query/results.jsonl`](data/68-query/results.jsonl) (one JSON object per
image) — see [`data/68-query/IMAGE_MAPPING_REPORT.md`](data/68-query/IMAGE_MAPPING_REPORT.md) for
field-by-field completeness. The 326-query screenshot evidence's manifest fields are documented in
[`data/326-query/google-images/README.md`](data/326-query/google-images/README.md) and
[`data/326-query/curify/README.md`](data/326-query/curify/README.md).

## 8. Image evidence

62 real screenshots (12 queries x 5 platforms, plus 2 backup captures for one query) are published
in [`data/68-query/images/`](data/68-query/images/), organized by platform. Every image is a
full-page SERP screenshot (not a single cropped result), so `organic_rank` is `null`/UNKNOWN by
design for all 62 — this is stated explicitly rather than guessed. Browse them all in the offline
gallery: **[`data/68-query/gallery/index.html`](data/68-query/gallery/index.html)** — filter by
query, platform, label, image type, or mapping confidence; works from a local double-click, no
server or internet connection required. See [`docs/68_IMAGE_SOURCE_INVENTORY.md`](docs/68_IMAGE_SOURCE_INVENTORY.md)
for exactly how this evidence was sourced and what's excluded, and
[`docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md`](docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md) for
the licensing status of the third-party screenshots (not CC BY 4.0 — see below).

**The 326-query benchmark now has real screenshot evidence for all 326 queries**, on two search
surfaces: [`data/326-query/google-images/`](data/326-query/google-images/) (326/326, Google
Images) and [`data/326-query/curify/`](data/326-query/curify/) (326/326, Curify — 318 standard
search-results pages, 1 genuine zero-result page, and 7 real captures of Curify's own deterministic
topic-category redirect for certain generic single-word queries, each explicitly tagged
`page_type=topic_redirect` and never presented as a standard search-results page). Browse them at
[`data/326-query/google-images/gallery.html`](data/326-query/google-images/gallery.html) and
[`data/326-query/curify/gallery.html`](data/326-query/curify/gallery.html). **This is unscored
visual evidence, not a new evaluation** — no relevance judgment, ranking, or score was generated
for either surface, and `evaluations.csv` (the scored Curify production-vs-candidate comparison)
was not re-run or altered.

## 9. Evaluation methodology

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full write-up. In short: 68-query uses a single-pass
LLM (Claude) relevance judge over automated Curify search-collection output, plus (for the 12-query
subset) a separate LLM visual review of the actual screenshot; 326-query uses a deterministic-rubric
LLM judge (`gpt-4o-mini`, temperature 0) over two pipeline code states. Neither includes completed
human review in this public release — see each dataset's README for exactly what was and wasn't
reviewed by a person.

## 10. Example comparisons

See [`docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md`](docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md) for
8 walked-through cases from the 12-query image subset — including cases where a competitor platform
also failed, and cases where an initial "content gap" finding was corrected after a manual re-check.

## 11. Use cases

- Visual/creative search and multimodal retrieval research.
- Ranking and recommendation-system evaluation.
- Regression testing of a search-relevance pipeline against a fixed query bank (326-query).
- Failure-mode analysis with visible evidence, not just aggregate scores (68-query image subset).
- Teaching/illustrating what "relevance," "recall," and "content gap" failures actually look like in
  a real product.

## 12. Known limitations

- 68-query cross-platform image evidence exists for only 12 of the 68 queries, not all 68. See
  section 8. The 326-query set now has screenshot evidence for all 326 queries (Google Images +
  Curify), but this is unscored visual evidence, not a relevance evaluation.
- Neither benchmark is a cross-platform *ranking* comparison; no numeric score exists for any
  non-Curify platform anywhere in this release — including the 326-query Google Images screenshots.
- Relevance labels are primarily LLM-judge output, not completed human review, in both benchmarks.
- The 326-query candidate branch was explicitly not approved for production at the time of capture —
  treat it as a regression-testing snapshot.
- Both are point-in-time snapshots; results will differ from current production Curify search.
- A separate, much larger 58-query x 5-platform pilot exists internally with **zero query overlap**
  with either published benchmark; it was deliberately not incorporated here (different query set —
  see `docs/68_IMAGE_SOURCE_INVENTORY.md` section 9) and is not part of this release.

## 13. Responsible use and attribution

- Query lists, schemas, evaluation labels, provenance docs, and code in this repository: **CC BY
  4.0** (see [`LICENSE`](LICENSE)) — free to use with attribution to Curify.
- The 50 third-party platform screenshots (Bing/Google/Canva/Pinterest) in
  `data/68-query/images/`: **not CC BY 4.0.** Included as benchmark evidence only; copyright remains
  with the original rights holders. Do not treat them as freely licensed for training, resale, or
  redistribution outside of citing this benchmark. Full rationale:
  [`docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md`](docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md).
- Do not present LLM-judge labels (`claude_relevance_label`, `visual_curify_label`,
  `relevance_label`) as human-reviewed ground truth — none of them are, in this release.

## 14. Repository structure

```
data/
  68-query/
    README.md                        per-dataset documentation
    queries.csv                      68 curated queries + curation metadata
    automated_relevance_labels.csv   Curify search collection + LLM relevance label
    schema.json                      field definitions
    provenance.json                  source hashes and transformation notes
    results.jsonl                    62 image-evidence records (12 of 68 queries)
    image_manifest.json              per-file hash/decode/duplicate inventory
    IMAGE_MAPPING_REPORT.md          confirmed/probable/unknown mapping breakdown
    images/<platform>/               62 screenshot files (curify/bing/google/canva/pinterest)
    gallery/index.html               offline, filterable image gallery
  326-query/
    README.md
    queries.csv                      326 queries with stable IDs (V001-V326)
    evaluations.csv                  production-baseline + candidate run results (652 rows)
    schema.json
    provenance.json
    google-images/                   326 Google Images screenshots + manifest + gallery
      README.md, manifest.csv, manifest.jsonl, gallery.html, screenshots/
    curify/                          326 Curify screenshots + manifest + gallery
      README.md, manifest.csv, manifest.jsonl, failed_queries.csv, gallery.html, screenshots/
docs/
  68_IMAGE_SOURCE_INVENTORY.md       read-only inventory of the image evidence sourcing
  EXAMPLE_CROSS_PLATFORM_COMPARISONS.md
  IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md
  release/PUBLICATION_COPY.md        draft HN/Reddit/LinkedIn copy (not auto-published)
scripts/
  validate_data.py                   CSV/schema/provenance validator
  validate_benchmark.py              adds image/gallery/hash/credential-scan checks
METHODOLOGY.md                       full methodology for both benchmarks
SOURCE_AUDIT.md                      source selection evidence and hashes
VALIDATION_REPORT.md                 result of the validation/QA pass for this release
SIZE_REPORT.md                       repo/image size accounting and large-file notes
DATASET_CARD.md                      structured dataset-card summary
```

## 15. How to use the dataset

```python
import pandas as pd
import json

q68 = pd.read_csv("data/68-query/queries.csv")
labels68 = pd.read_csv("data/68-query/automated_relevance_labels.csv")

# 68-query image evidence (12 of 68 queries, 62 records)
image_records = [json.loads(l) for l in open("data/68-query/results.jsonl", encoding="utf-8")]

q326 = pd.read_csv("data/326-query/queries.csv")
evals326 = pd.read_csv("data/326-query/evaluations.csv")
evals326.groupby("run_variant")["relevance_label"].value_counts()

# 326-query screenshot evidence (326/326 each, unscored)
google_manifest = pd.read_csv("data/326-query/google-images/manifest.csv")
curify_manifest = pd.read_csv("data/326-query/curify/manifest.csv")
curify_manifest["page_type"].value_counts()  # search_results / search_zero_results / topic_redirect
```

Or just open [`data/68-query/gallery/index.html`](data/68-query/gallery/index.html),
[`data/326-query/google-images/gallery.html`](data/326-query/google-images/gallery.html), or
[`data/326-query/curify/gallery.html`](data/326-query/curify/gallery.html) directly in a browser —
no setup required.

### Validation

```
python3 scripts/validate_data.py       # CSV/schema/provenance checks
python3 scripts/validate_benchmark.py  # image hashes, gallery refs, duplicate/credential scans
```

See [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) for the result recorded at release time.

## 16. Citation

See [`CITATION.cff`](CITATION.cff).

## 17. Contributing

This is a static, point-in-time data release rather than an actively-developed codebase. If you find
a data-quality issue (a mismapped image, a hash mismatch, a broken gallery reference), please open an
issue describing the specific file and record — run `scripts/validate_benchmark.py` first, since it
catches most structural issues automatically. Pull requests that add new *unverified* query/platform/
rank/label mappings will not be accepted without the same evidence-and-hash standard used throughout
this repository (see `docs/68_IMAGE_SOURCE_INVENTORY.md` for what that standard looks like in
practice).

## About Curify

[Curify AI](https://curify-ai.com) is an applied-AI company building the **deterministic production layer above foundation models** — reliable, traceable, enterprise-grade pipelines, not a prompt wrapper. Our products span two lines:

- **Enterprise AI** — an industrial-grade multimodal content engine + enterprise **document intelligence** (RAG with mandatory source citation, structured extraction, on-premise; *deterministic · traceable · data stays yours*).
- **AI-Native Product** — creator / SMB-facing generation at [curify-ai.com](https://curify-ai.com): structured data & long-tail keywords → thousands of on-brand visual assets, multilingual video, and one-click design tools.

**Links** · Website: [curify-ai.com](https://curify-ai.com) · Mentorship (founder, Jay Wang): [mentorcruise.com/mentor/jaywang](https://mentorcruise.com/mentor/jaywang/)
