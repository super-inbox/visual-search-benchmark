# Dataset Card: Visual Search Benchmark

## Dataset summary

Two Curify-internal search-evaluation datasets, converted for public release:

- **68-query benchmark** — 68 hand-curated queries evaluating Curify's own visual/design search,
  plus real cross-platform screenshot evidence (Curify/Bing/Google/Canva/Pinterest) for 12 of the
  68 queries.
- **326-query benchmark** — 326 queries used to regression-test two code states of Curify's own
  search-relevance pipeline. No cross-platform data of any kind.

They are published together because they came from the same internal search-quality effort, but
they are **not a single unified benchmark** — different query sets, different systems under test,
different label vocabularies, different amounts of image evidence. See `METHODOLOGY.md`.

## Supported tasks

- Visual/creative search relevance evaluation
- Cross-platform retrieval comparison (12-query image subset only — qualitative, not scored)
- Search-relevance regression testing (326-query, production vs. candidate pipeline)
- Failure-mode / error analysis for image and design search systems
- LLM-as-judge methodology study (both benchmarks use an LLM judge, with documented rubrics)

**Not supported / not intended:** training a cross-platform ranking model directly off this data (no
platform besides Curify has a scored, ranked signal); claiming this is a complete or industry-
standard visual-search benchmark; treating any label here as human-reviewed ground truth.

## Languages

- 68-query: English (34), Chinese (28), mixed (6).
- 326-query: Chinese (163), English (163), an exact 50/50 split by design.
- Query text is not translated or normalized — published verbatim in its original language.

## Dataset structure

```
data/68-query/    queries.csv, automated_relevance_labels.csv, schema.json, provenance.json,
                  results.jsonl, image_manifest.json, IMAGE_MAPPING_REPORT.md, images/, gallery/
data/326-query/   queries.csv, evaluations.csv, schema.json, provenance.json
```

### Data instances

**68-query, `queries.csv` row:** one curated query with scene/priority/curation metadata.
**68-query, `automated_relevance_labels.csv` row:** one query's automated Curify search-collection
result plus an LLM relevance label.
**68-query, `results.jsonl` record:** one *image* (one query x one platform x one capture), with
mapping-confidence and evaluation fields — see field list below.
**326-query, `evaluations.csv` row:** one query x one run_variant (production baseline or candidate
branch) evaluation result.

### Data fields

Authoritative field lists: `data/68-query/schema.json`, `data/326-query/schema.json`. The
68-query image-evidence record (`results.jsonl`) fields:

| Field | Notes |
|---|---|
| `benchmark_id`, `query_id`, `query`, `query_language`, `query_category` | Joins back to `queries.csv`; `query_language` is derived (Unicode-range detection), not source-provided. |
| `platform` | One of `curify`, `bing`, `google`, `canva`, `pinterest`. |
| `organic_rank` | Always `null` in this release — every image is a full-page screenshot, not a single ranked result. |
| `image_type` | Always `serp_screenshot` in this release. |
| `image_path`, `thumbnail_path` | Repo-relative paths, never local absolute paths. |
| `original_source_filename` | The filename as it existed in the (non-public) source repo. |
| `source_page_url` | Populated for `curify` rows only (12 of 62); `null` elsewhere — no such URL exists in the source data for the other platforms. |
| `image_source_url` | `null` for all 62 — not recorded anywhere in source data. |
| `captured_at` | Date only (`2026-07-07` or `2026-07-09`), taken from explicit statements in the source notes. |
| `evaluation_label`, `evaluation_reason` | Populated for `curify` rows (12/62, all `FAIL`); `null`/free-text-only for the 50 competitor-platform rows (no formal label exists for those). |
| `source_sha256`, `published_sha256` | Identical for every record — images were copied byte-for-byte, never edited. |
| `mapping_confidence` | `confirmed` for all 62 (see `IMAGE_MAPPING_REPORT.md` for the evidence chain); the schema also supports `probable`/`unknown` for future extensions, unused in this release. |
| `mapping_evidence`, `notes` | Free text explaining the confidence call and any capture-process caveats (re-captures, backups, stale-status corrections). |

### Data splits

Neither dataset has a train/test split — both are evaluation-only snapshots of a search system at a
point in time, not training data.

## Dataset creation

### Source data

Both benchmarks were converted from an internal (non-public) Curify evaluation working repository.
See `SOURCE_AUDIT.md` for exact source file names, SHA-256 hashes, and the selection rationale among
multiple candidate source files. See `docs/68_IMAGE_SOURCE_INVENTORY.md` for the image-evidence
sourcing specifically, including what was found but explicitly excluded (a 58-query, 5-platform
pilot with zero query overlap with either published benchmark; a 68-query "human review" column
that turned out to be LLM-generated despite its name).

### Annotations

- 68-query relevance labels: single-pass LLM (Claude) judgment over automated search-collection
  output, plus (12-query subset only) a separate LLM visual review of the actual screenshot.
- 326-query relevance labels: LLM judge (`gpt-4o-mini`, temperature 0, deterministic rubric) over
  top-5 results per query per run variant.
- No completed human review is included in this public release for either benchmark.

### Personal and sensitive information

Query text and screenshots may incidentally depict publicly-available third-party web content (blog
posts, marketplace listings, social posts) as it appeared in search results at capture time; no
private accounts, login credentials, cookies, or personal data were knowingly captured, and image
files were scanned for local absolute paths, tokens, and credential-shaped strings before
publication (see `SOURCE_AUDIT.md` and `docs/68_IMAGE_SOURCE_INVENTORY.md` section 7 — no matches
found in the published image set).

## Considerations for using the data

### Social impact / biases

Query curation and scene/scenario labeling were done by Curify's own team for its own product
evaluation; the query set reflects the use cases Curify chose to test (brand, marketing/e-commerce,
education, cultural-creative), not a neutral or exhaustive sample of visual-search use cases.

### Other known limitations

See root `README.md` section 12 and each dataset's own `README.md`.

## Licensing

- Query lists, schemas, provenance, evaluation labels/reasons, documentation, and code: **CC BY
  4.0** (`LICENSE`), attribution to Curify.
- The 50 third-party platform screenshots (Bing/Google/Canva/Pinterest) in
  `data/68-query/images/`: **not CC BY 4.0** — evidence-only inclusion, rights remain with original
  holders. See `docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md`.

## Additional information

- **Dataset curators:** Curify (internal search-quality team).
- **Citation:** `CITATION.cff`.
- **Version:** `1.1.0`, released 2026-07-31 (68-query image evidence added; original data release
  was `1.0.0`, 2026-07-30).
- **Contact/issues:** open a GitHub issue on this repository; see `README.md` "Contributing."
