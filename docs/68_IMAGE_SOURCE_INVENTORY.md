# 68-query image source inventory

Read-only inventory of cross-platform image/screenshot evidence found in the internal source
repository (`visual-search-adhoc`, not itself public) that is genuinely tied to the published
68-query gold set. No source files were moved, edited, or deleted to produce this report.

## Summary

**Cross-platform image evidence exists for 12 of the 68 published queries, not all 68.** This is
a hard constraint of the source data, not a publishing choice — no equivalent evidence exists for
the other 56 queries anywhere in the source repo. See "Rejected / out-of-scope image sources"
below for the other image-shaped artifacts that were considered and excluded.

| Metric | Value |
|---|---|
| Queries with cross-platform image evidence | 12 of 68 (`q002, q006, q009, q010, q015, q016, q034, q046, q053, q060, q064, q068`) |
| Platforms per query | 5: Curify, Bing Images, Google Images, Canva, Pinterest |
| Image files found on disk | 75 (60 primary + 2 backup/extra Curify captures for `q015` + 12 `notes.md` + 1 stray `.DS_Store`) |
| Image files copied into public repo | 62 (all 60 primary + both `q015` extras; `notes.md`/`.DS_Store` are not images and were not copied) |
| Format | PNG only |
| Total size (source) | ~158 MB across the 62 copied files |
| Decodable | 62 / 62 (100%) — verified with Pillow `Image.verify()` + re-open |
| Corrupted/truncated | 0 |
| Duplicate images (identical SHA-256) | 1 pair: `q015` `curify1.png` == the published `curify.png` (see below) |
| Confirmed query_id mapping | 62 / 62 (100%) |
| Confirmed platform mapping | 62 / 62 (100%) |
| Confirmed organic rank | 0 / 62 — see "Why rank is UNKNOWN" below |
| Unmappable images | 0 |
| Mapping evidence source | Source-repo `notes.md` per-query files (explicit "Screenshot Paths" section) + a source-repo cross-check document (`P0_SCREENSHOT_INDEX_2026-07-14.md`) + independent re-verification against the *published* `queries.csv` by exact query-text match (done by this tool, not merely trusted from source docs) |
| Screenshots vs. single result images | All 62 are full-page/full-viewport SERP screenshots. None are single cropped result images. |
| Sensitive info found in this specific asset | None (explicitly re-scanned; see below) |

## 1. Source files found

- **Image files:** `docs/daily_report/7.9/competitor_screenshots/<query-slug>/{curify,bing,google,canva,pinterest}.png`, 12 query-slug directories. One directory (`k_beauty_glass_skin_brand_launch_visual`) additionally contains `curify1.png` and `curify2.png` (manual re-capture backups).
- **Per-query annotation files:** `docs/daily_report/7.9/competitor_screenshots/<query-slug>/notes.md` — free-text query intent, an LLM (Claude) "Visual Review" of the Curify screenshot (label + reason), and a "Competitor Screenshot Results" section with one free-text observation per competitor platform, a "best competitor platform" call, and an "updated conclusion." No numeric scores anywhere.
- **Query list / slug key:** `docs/daily_report/7.9/manual_review/external_screenshot_queries_12_2026-07-09.csv` — the authoritative list of which 12 queries this asset covers (`query, safe_query_slug, primary_scene, secondary_scene, issue_type, platforms_to_capture, canva_fallback_query`).
- **Query-ID cross-check:** `docs/daily_report/7.14/search-relevance-stage7-rerun/p0-12-before-after/P0_SCREENSHOT_INDEX_2026-07-14.md` — maps each of the 12 slugs to a `Q02`…`Q68` identifier. This report independently re-verified every one of these 12 mappings by exact-text match against the *published* `queries.csv` (not by trusting the source doc's own claim) — all 12 matched exactly, with no discrepancies.
- **Stale/superseded status file:** `docs/daily_report/7.9/manual_review/P0_visual_review_with_claude_2026-07-09.csv` — an earlier LLM-generated visual-observation CSV whose `competitor_screenshots_available` column says "No" / "Pending" for all 12 rows, even though the competitor screenshots were captured later the same day and do exist on disk. This CSV is stale relative to the `notes.md` files and was **not** used as a data source for this release — the per-query `notes.md` files (which postdate it) were used instead.
- **Completeness/QA docs:** `docs/daily_report/7.9/COMPETITOR_SCREENSHOT_INDEX_2026-07-09.md` and `COMPETITOR_SCREENSHOT_FINAL_CHECK_2026-07-09.md` — internal QA notes confirming 72/72 expected files present and documenting two Canva screenshots that were re-captured after an initial mid-load capture.
- **Collector script (not data):** `scripts/external-screenshot-p0-12/collect.mjs` — the Playwright collector used for the automated Bing/Google/Canva captures.

## 2. Per-platform image counts (this asset only)

| Platform | Images found | Images copied |
|---|---|---|
| Curify | 14 (12 primary + 2 backups for `q015`) | 14 |
| Bing | 12 | 12 |
| Google | 12 | 12 |
| Canva | 12 | 12 |
| Pinterest | 12 | 12 |
| **Total** | **62** | **62** |

## 3. Format, size, decodability

- All 62 files are valid PNG (confirmed with Pillow `Image.verify()` and a second open pass to read
  dimensions — both must succeed for `decodable: true`).
- Resolutions vary: ~1440x1000–1440x2178 for most automated/full-page captures; up to ~3024x2178
  for a few manually re-captured Retina-display screenshots.
- Total size of the 62 copied files: **~158 MB**. See `SIZE_REPORT.md` for repo-size implications.
- 0 corrupted, 0 truncated, 0 zero-byte files.

## 4. Duplicates

One exact duplicate pair by SHA-256: for query `q015` (K-beauty glass skin brand launch visual),
the source folder's `curify.png` is byte-identical to `curify1.png` (per the source `notes.md`,
`curify.png` was created by copying `curify1.png`). Both are published — `curify1.png` as a labeled
backup capture, `curify2.png` (a different, scrolled-view capture, not a duplicate) also published —
per the "don't lose files on name conflicts" requirement. See `IMAGE_MAPPING_REPORT.md` for the
exact file list.

## 5. Mapping confidence

**All 62 images: `confirmed` query_id, `confirmed` platform.** Evidence chain:

1. The source repo's `external_screenshot_queries_12_2026-07-09.csv` names the 12 queries and their
   folder slugs.
2. Each folder's `notes.md` explicitly states which platform each `.png` file in that folder belongs
   to (a "Screenshot Paths" section naming `curify.png`, `bing.png`, etc. individually).
3. A separate, later source document (`P0_SCREENSHOT_INDEX_2026-07-14.md`) independently maps each
   of the 12 slugs to a gold-set ID (`Q02` etc.).
4. This tool independently re-derived the same mapping a third way: it matched each of the 12 query
   texts verbatim against the *already-published* `data/68-query/queries.csv` and confirmed all 12
   land on the exact `query_id` the source doc claims (0 mismatches). This third, independent check
   is why confidence is `confirmed` rather than `probable`.

**Organic rank: `null`/UNKNOWN for all 62 images — by design, not by omission.** Every image in this
asset is a full-page/full-viewport screenshot of an entire result grid or search page, not a crop of
a single ranked result. No source document assigns a rank number to any individual result within
these screenshots. Marking rank as UNKNOWN is therefore the correct and only honest value; it is not
a gap to be guessed at.

**Evaluation label:** `evaluation_label` is populated (`FAIL`, cross-checked against the already
published `claude_relevance_label` in `automated_relevance_labels.csv` — all 12/12 match) only for
the `curify` platform, where a specific LLM-generated `visual_curify_label` exists in `notes.md` tied
directly to that screenshot. For the four competitor platforms, no equivalent formal label exists —
only free-text "observation" prose. `evaluation_label` is left `null` for those 50 images; the prose
is preserved verbatim (lightly re-punctuated) in `evaluation_reason`.

## 6. Image type

All 62 images are labeled `image_type: "serp_screenshot"` — confirmed both by the source's own
description ("single full-page screenshot... no separate top-region crop exists," per
`P0_SCREENSHOT_INDEX_2026-07-14.md`) and by the `notes.md` prose, which repeatedly describes "the
rendered result grid" / "the banner" / multiple visible cards per screenshot. None are single
isolated result images.

## 7. Sensitive information / local paths

Re-scanned specifically for this 12-query asset (`docs/daily_report/7.9/competitor_screenshots/` and
`docs/daily_report/7.9/manual_review/`): **no hits** for local absolute paths (`/Users/`, `/home/`),
loopback addresses, tokens, API keys, cookies, or email addresses. One in-repo note (in the source's
own `P0_SCREENSHOT_INDEX_2026-07-14.md`) explicitly states that a red numeric badge visible in the
corner of some Curify screenshots is a local Next.js dev-tool overlay, not sensitive data, and is
purely cosmetic — noted here for transparency, no image was altered to remove it.

A **separate, unrelated** dataset in the same source repo (`docs/external-signal-pilot/*-58/`, a
58-query pilot — see below) does contain ~305 hits of a local absolute path
(`/Users/<username>/Desktop/curify-frontend/...`) inside its JSON/CSV manifests. That dataset was
**not copied** into this release (see below), so none of that path leakage is present in the public
repo.

## 8. Suggested public directory structure (as implemented)

The existing repo already organizes each benchmark under `data/<name>-query/`, so this release adds
to that structure rather than introducing a new top-level `benchmarks/` tree:

```
data/68-query/
  images/
    curify/    (14 files)
    bing/      (12 files)
    google/    (12 files)
    canva/     (12 files)
    pinterest/ (12 files)
  gallery/
    index.html
    thumbnails/<platform>/*.jpg
  image_manifest.json
  results.jsonl
  IMAGE_MAPPING_REPORT.md
```

## 9. Rejected / out-of-scope image sources (found, but not used for the 68-query benchmark)

- **`docs/external-signal-pilot/{bing,google,canva,curify,pinterest}-search-eval-58/`** — a much
  larger, more structurally rich, ranked cross-platform pilot (58 queries x 5 platforms, ~590 image
  files, ~620 MB, with full per-result rank/title/URL manifests in `data/per-query/*.json`). **Zero
  of its 58 queries exact-text-match any of the 68 published gold queries** (verified programmatically
  against `queries.csv`) — it is a genuinely different query set. Per explicit user direction, it is
  **not** incorporated into the 68-query benchmark and not published in this release. It also contains
  ~305 local-absolute-path leaks in its JSON manifests that would need scrubbing before any future
  publication.
- **`docs/daily_report/7.14/.../hard_queries_manual_review_68_2026-07-14.csv`** — a fully-populated
  "human_relevance_label" column over the same 68 queries, but its own `reviewer_type` column reads
  `CLAUDE_STRUCTURED_TOP10_REVIEW` for all 68 rows — i.e., LLM-generated, not human-reviewed, despite
  the column name. Confirms the exclusion already recorded in `SOURCE_AUDIT.md`. Not used.
- **`docs/daily_report/7.14/.../p0-12-before-after/`** — a Curify-only (not cross-platform)
  before/after comparison for the same 12 queries (2026-07-07 vs. 2026-07-14 production). Related to,
  but distinct from, the cross-platform asset used here. Not published (out of scope for this release;
  it does not add cross-platform evidence).
