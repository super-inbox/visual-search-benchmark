# Validation Report

Generated 2026-07-31 for the `v1.1.0` update (adds the 68-query cross-platform image evidence for
12 of the 68 queries). The original `v1.0.0` (2026-07-30, no images) validation results are
preserved below where still applicable; this report reflects actual output from running both
`scripts/validate_data.py` and `scripts/validate_benchmark.py`, not expected/assumed results.

## Public file list (new/changed since `v1.0.0`)

```
DATASET_CARD.md                                  (new)
LICENSE                                          (updated -- third-party image scope carve-out)
CITATION.cff                                     (version bumped 1.0.0 -> 1.1.0)
README.md                                        (restructured, gallery/image sections added)
METHODOLOGY.md                                   (68-query image section updated)
SOURCE_AUDIT.md                                  (12-query subset marked as now-published)
SIZE_REPORT.md                                   (new)
docs/68_IMAGE_SOURCE_INVENTORY.md                (new)
docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md       (new)
docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md      (new)
docs/release/PUBLICATION_COPY.md                 (new, drafts only, not published)
scripts/validate_benchmark.py                    (new)
data/README.md                                   (updated)
data/68-query/README.md                          (updated)
data/68-query/results.jsonl                      (new, 62 records)
data/68-query/image_manifest.json                (new)
data/68-query/IMAGE_MAPPING_REPORT.md             (new)
data/68-query/images/{curify,bing,google,canva,pinterest}/  (new, 62 files, ~158 MB)
data/68-query/gallery/index.html                 (new)
data/68-query/gallery/thumbnails/<platform>/      (new, 62 JPEG thumbnails, ~2.6 MB)
data/326-query/README.md                         (updated -- explicit "no images" note)
```

Unchanged from `v1.0.0`: `data/68-query/queries.csv`, `automated_relevance_labels.csv`,
`schema.json`, `provenance.json`; all of `data/326-query/` except `README.md`;
`scripts/validate_data.py` (logic unchanged).

## `scripts/validate_data.py` result

```
python3 scripts/validate_data.py
```

**OVERALL: PASS** (exit code 0). Covers: required-file presence, UTF-8 validity, CSV/JSON parse,
query counts (68 / 326), duplicate/empty query detection, schema-header conformance, provenance-hash
consistency, label-vocabulary and label-distribution conformance for both benchmarks, and a
sensitive-string/forbidden-file sweep over the original (non-image) file set.

## `scripts/validate_benchmark.py` result (new script, image/gallery-focused)

```
python3 scripts/validate_benchmark.py
```

**OVERALL: PASS** (exit code 0). Full stats block from the run:

| Metric | Value |
|---|---|
| 68-query count | 68 |
| 326-query count | 326 |
| `results.jsonl` records | 62 |
| `image_manifest.json` image_count | 62 (matches) |
| Images per platform | curify 14, bing 12, google 12, canva 12, pinterest 12 |
| `mapping_confidence` counts | confirmed 62, probable 0, unknown 0 |
| Broken/undecodable images | 0 |
| Duplicate `image_path` values | 0 |
| Duplicate (query_id, platform, organic_rank) triples | 2 (both `q015`/`curify`/`null` -- the documented `curify.png`/`curify1.png` byte-identical pair plus the distinct `curify2.png` backup sharing the same triple; see `IMAGE_MAPPING_REPORT.md` "Duplicate images") |
| SHA-256 mismatches (published vs. recorded) | 0 |
| Gallery embedded records | 62 |
| Gallery broken image/thumbnail references | 0 |
| External references in gallery HTML (CDN/remote script/font/fetch) | 0 |
| 326-query images/ directory present (must be absent) | absent -- confirmed |
| 326-query docs/schema files falsely claiming an image file | 0 |

Checks performed: JSONL parse validity per line, required-field presence per image record,
`organic_rank` type enforcement (integer or `null`, never a string), `query_id` referential
integrity against `queries.csv`, `mapping_confidence` vocabulary enforcement (`confirmed` /
`probable` / `unknown` only, with `mapping_evidence` required whenever `probable`), image-path
existence and decodability (Pillow verify + load), SHA-256 recomputation against
`published_sha256`, duplicate-path and duplicate-triple detection, gallery HTML external-reference
scan, gallery embedded-JSON-vs-disk cross-check, an explicit assertion that `data/326-query/`
has no `images/` directory and its docs/schema files don't claim any image file that doesn't exist
on disk, a repo-wide local-absolute-path / loopback-reference / credential-shaped-string sweep
(tightened to require assignment-like context for common-English-word patterns such as "secret,"
avoiding false positives on quoted result titles like "The Secret to Korean Glass Skin"), and a
UTF-8 validity check across `.md`/`.csv`/`.json`/`.jsonl`/`.html` files repo-wide.

## Query, language, category/scenario counts

Unchanged from `v1.0.0`: **68-query:** 68 unique queries, 0 duplicates, 0 empty; English 34 /
Chinese 28 / mixed 6; scene brand 19 / marketing-ecommerce 18 / education 17 / cultural-creative 14.
**326-query:** 326 unique queries, 0 duplicates, 0 empty; 163 zh / 163 en; scenario creative_merch 82
/ brand_business 82 / marketing_ecommerce 82 / education 80.

## Status / label distributions

**68-query** (`claude_relevance_label`, all 68): FAIL 43, WARN 25, PASS 0 -- unchanged.

**68-query image subset** (`evaluation_label` in `results.jsonl`, `curify` platform only, 12
records): FAIL 12, WARN 0, PASS 0 (these 12 queries were pre-selected as already-flagged cases in
the source pilot -- see `docs/68_IMAGE_SOURCE_INVENTORY.md`; not representative of the full-68
distribution above). The 50 competitor-platform records have `evaluation_label: null` by design (no
formal label exists in source data for those).

**326-query** (`relevance_label`, by `run_variant`) -- unchanged:

| run_variant | PASS | PARTIAL | FAIL | UNJUDGABLE | zero_result | low_result |
|---|---|---|---|---|---|---|
| production_baseline_2026-07-21 | 24 | 83 | 207 | 12 | 23 | 19 |
| candidate_2026-07-22_0e794cd9 | 38 | 86 | 195 | 7 | 20 | 18 |

## Referential integrity

- 68-query: all 68 `automated_relevance_labels.csv` rows join to a `queries.csv` query_id (unchanged).
- 68-query images: all 62 `results.jsonl` records join to a `queries.csv` query_id; all 12 covered
  query_ids (`q002, q006, q009, q010, q015, q016, q034, q046, q053, q060, q064, q068`) confirmed
  present in `queries.csv` with matching query text (see `IMAGE_MAPPING_REPORT.md`).
- 326-query: both `evaluations.csv` run variants (326 rows each, 652 total) join fully to
  `queries.csv` query_id (unchanged); confirmed no `images/` directory and no false image-file
  claims in its docs/schema.

## Sensitive-data scan

Ran the pattern sweep from both validator scripts across every staged file. Local-absolute-path,
loopback-reference, and credential-shaped-string patterns are defined in
`scripts/validate_benchmark.py`'s `SENSITIVE_PATTERNS` (not repeated verbatim here to avoid the
report re-triggering its own scanner). **Result: clean**, with two previously-reviewed, documented
false positives carried forward / added:

1. (from `v1.0.0`) the substring `sk-` inside the public Curify template slug
   `elon-musk-tech-meme` in `SOURCE_AUDIT.md` -- confirmed not a credential.
2. (new) a redacted `<username>` placeholder in `docs/68_IMAGE_SOURCE_INVENTORY.md`, used to
   describe (without disclosing) a real local-path leak found in the **unpublished** 58-query pilot
   dataset -- confirmed intentionally redacted, not a live leak in this repo.

The 62 newly-published images and their `notes.md`-derived text were separately scanned in
`docs/68_IMAGE_SOURCE_INVENTORY.md` section 7 -- clean, no local paths, tokens, or cookies found.

## Repo size

See `SIZE_REPORT.md`. Summary: ~158 MB of new image files (62 PNGs), ~2.6 MB of new thumbnails (62
JPEGs). No individual file exceeds GitHub's 50 MB soft-warning threshold or its 100 MB hard limit;
the largest published image is approximately 7.4 MB. No file was compressed, cropped, or otherwise
degraded to reduce size.

## Known limitations

See each dataset's `README.md`, `DATASET_CARD.md`, and the root `METHODOLOGY.md`. In summary:
cross-platform image evidence exists for only 12 of the 68 queries (not all 68, and not at all for
326-query as of this `v1.1.0` snapshot — this limitation was superseded for the 326-query screenshot
evidence by the `v1.2.0` update below, which added unscored Google Images and Curify screenshot
evidence for all 326 queries); neither benchmark includes completed human review in this release;
the 326-query candidate branch was not approved for production at capture time; all data is a
point-in-time snapshot.

## Overall result (`v1.1.0`, 68-query image evidence)

- `python3 scripts/validate_data.py` -> **PASS** (exit code 0)
- `python3 scripts/validate_benchmark.py` -> **PASS** (exit code 0)
- Sensitive-data scan -> clean (two reviewed false positives, documented above)
- Image hash verification -> 62/62 `published_sha256` match recomputed SHA-256, 0 mismatches
- Image decode verification -> 62/62 decodable, 0 broken
- Gallery reference verification -> 62/62 full-image and thumbnail references resolve, 0 broken

**OVERALL: PASS**

## Update: `v1.2.0` (2026-08-03) — 326-query Google Images + Curify screenshot evidence

Adds real, unedited screenshot evidence for all 326 queries on two search surfaces:
`data/326-query/google-images/` (326/326) and `data/326-query/curify/` (326/326: 318 standard
search-results pages, 1 genuine zero-result page, 7 verified topic-redirect pages). This is
evidence only — `queries.csv` and `evaluations.csv` (and their hashes in `provenance.json`) are
unchanged; the label distributions and referential-integrity results reported above for the
326-query benchmark still hold as-is.

### Public file list (new since `v1.1.0`)

```
LICENSE                                          (updated -- 326-query third-party/first-party image scope carve-out)
CITATION.cff                                     (version bumped 1.1.0 -> 1.2.0)
README.md                                        (326-query image-evidence sections added)
METHODOLOGY.md                                   (326-query screenshot-evidence section added)
SOURCE_AUDIT.md                                  (326-query screenshot-evidence source entry added)
SIZE_REPORT.md                                   (326-query update section added)
DATASET_CARD.md                                  (structure, licensing, version updated)
scripts/validate_data.py                         (326-query manifest checks added, human_spot_check.csv guard added)
scripts/validate_benchmark.py                    (326-query image/gallery checks replace the old "no images" guard)
data/README.md                                   (updated)
data/326-query/README.md                         (image-evidence sections added, "no images" claim removed)
data/326-query/provenance.json                   (image_evidence block + 2 manifest hashes + limitations updated)
data/326-query/google-images/                    (new: README.md, manifest.csv, manifest.jsonl, gallery.html, screenshots/ [326 JPEG, ~83 MB])
data/326-query/curify/                           (new: README.md, manifest.csv, manifest.jsonl, failed_queries.csv, gallery.html, screenshots/ [326 JPEG, ~60 MB])
```

Unchanged: `data/326-query/queries.csv`, `evaluations.csv`, `schema.json` (field lists for those
two CSVs); all of `data/68-query/`.

### `scripts/validate_data.py` result

```
python3 scripts/validate_data.py
```

**OVERALL: PASS** (exit code 0). New checks exercised: required-file presence for
`data/326-query/{google-images,curify}/*`, `human_spot_check.csv` absence sweep (repo-wide),
326/326 row-count and query_id referential-integrity for both new manifests (against
`queries.csv`), duplicate `query_id` / duplicate `screenshot_path` detection, screenshot-path
existence and no-local-absolute-path checks, orphan-screenshot detection (files on disk not
referenced by the manifest), all-rows-`status=success` assertion for both manifests, and
`curify/failed_queries.csv` header-only (0 data rows) assertion.

### `scripts/validate_benchmark.py` result

```
python3 scripts/validate_benchmark.py
```

**OVERALL: PASS** (exit code 0). New stats from this run:

| Metric | google-images | curify |
|---|---|---|
| Decoded | 326 | 326 |
| Broken/undecodable | 0 | 0 |
| Wrong format (not real JPEG) | 0 | 0 |
| Wrong dimensions | 0 | 0 |
| Dimension distribution | `1440x1000`: 326 | `1440x900`: 326 |
| Gallery `<img>` tags | 326 | 326 |
| Gallery broken references | 0 | 0 |

Checks performed (new `check_326query_images()`, replacing the old `check_326_no_image_claims()`
guard that asserted no images could exist): per-file Pillow `verify()` + `load()` decode,
actual-format-vs-`.jpg`-extension match (catches a PNG-saved-as-`.jpg` mismatch, which is exactly
what an earlier, superseded manual-capture attempt for 7 Curify queries had — see
`data/326-query/curify/README.md`), exact-dimension match against each platform's fixed
viewport/capture size, gallery HTML external-reference scan (no CDN/remote script/font), and
gallery embedded-`<img src>`-vs-disk cross-check. Sensitive-string scan (`scan_text_for_sensitive`)
also ran across both new `gallery.html` files and all new manifest/README files as part of the
existing repo-wide sweep -- clean.

### Manual visual spot-check (this update)

Per the task's own requirement that "file exists" is not the same as "content verified": every
one of the 7 Curify `topic_redirect` captures was individually opened and visually confirmed (page
body rendered, results grid present and topically consistent with the query, correct final URL, no
error/blank/loading page, no browser-chrome-only capture) -- see the table in
`data/326-query/curify/README.md`. Google Images: first query (V001), last query (V326), one
Chinese mid-range query (V163), and the smallest-file-size outlier (V290, "whiteboard", checked
specifically to rule out a blank/near-blank page) were all individually visually confirmed as real,
correct Google Images results pages -- no consent wall, CAPTCHA, or error page in any of them
(consistent with `consent_detected=false` / `captcha_detected=false` on all 326 manifest rows).

### Sensitive-data / public-safety scan (this update)

Clean. No local absolute paths, no `human_spot_check.csv`, no cookies/tokens/credential-shaped
strings in either new screenshot set or its manifests/READMEs/gallery HTML.

### Repo size (this update)

See `SIZE_REPORT.md`. Summary: ~144 MB of new files (652 JPEG screenshots + manifests + galleries
+ docs), largest individual file 398 KB -- far under GitHub's 50 MB/100 MB thresholds, no LFS
required.

### Overall result (`v1.2.0`)

- `python3 scripts/validate_data.py` -> **PASS** (exit code 0)
- `python3 scripts/validate_benchmark.py` -> **PASS** (exit code 0)
- 326-query Google Images evidence -> 326/326, all decodable, all `1440x1000` real JPEG, 0 broken
  gallery references
- 326-query Curify evidence -> 326/326, all decodable, all `1440x900` real JPEG, 0 broken gallery
  references, 7 explicitly-labeled `topic_redirect` pages individually visually verified
- `human_spot_check.csv` -> absent repo-wide, confirmed
- Sensitive-data scan -> clean

**OVERALL: PASS**
