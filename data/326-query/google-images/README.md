# Google Images screenshot evidence — 326-query set

Real, unedited Google Images search-results screenshots for all 326 queries in
[`../queries.csv`](../queries.csv) (`query_id` `V001`-`V326`). This is **visual evidence of
what Google Images actually returned**, captured 2026-08-01/02 — not a relevance judgment, not a
score, and not part of `evaluations.csv` (which evaluates Curify only, per
[`../../../METHODOLOGY.md`](../../../METHODOLOGY.md)).

## At a glance

- **Coverage:** 326 of 326 queries (100%), 0 failures.
- **Platform:** Google Images (`google.com/search?tbm=isch`), not Curify.
- **Captured:** 2026-08-01 to 2026-08-02.
- **Format:** JPEG, quality 80, exactly 1440x1000, single first-viewport screenshot (no
  scrolling, no per-result cropping).
- **Every record is `status=success`** — no CAPTCHA, consent wall, or blocked page was ever
  retained as evidence; see "Collection method" below for how transient errors during
  collection were handled (all resolved by retry before the final manifest, never bypassed).

## Files

| File | Rows | Description |
|---|---|---|
| `manifest.csv` / `manifest.jsonl` | 326 each | One row per query: URL, screenshot path, status, timing, attempt count. Field-for-field identical between the two formats. |
| `screenshots/` | 326 JPEGs | `V001__query.jpg` style filenames (query_id + ASCII slug of the query text; non-ASCII/short queries fall back to a `query` placeholder slug — the `query_id` is always the authoritative key, not the filename). |
| `gallery.html` | - | Offline, self-contained gallery — open directly in a browser, no server needed. |

## Manifest fields

`query_id, source_row, query, platform, search_url, screenshot_path, status, page_status,
consent_detected, captcha_detected, attempt_count, started_at, completed_at, duration_ms,
error_type, error_message, collector_version, input_sha256`

- `platform` is always `google_images`.
- `search_url` is the literal request URL: `https://www.google.com/search?tbm=isch&q=<query>&hl=en`.
- `consent_detected` / `captcha_detected` are `false` for all 326 records in the final manifest —
  no query was collected past an unresolved consent wall or CAPTCHA (see below).
- `input_sha256` matches `../queries.csv`'s SHA-256 (`d8ae0f4ef77567b4dcf8f15635b11c140810c3b991a8134a99997e11ad6a1d9e`) on every row.

## Collection method

- Playwright, Chromium, headed, `launchPersistentContext` (real browser profile, not
  headless/stealth-patched); viewport/screenshot 1440x1000; concurrency 1; randomized
  7,000-13,000ms delay between queries; 60,000ms navigation timeout.
- Consent walls: only a standard "Accept all" / "I agree" button click, if presented — the
  collector never scraped past an unresolved consent wall.
- CAPTCHA: detection only. The collector is designed to stop after 3 consecutive CAPTCHA
  detections and never bypasses one. Zero CAPTCHA challenges appear in the final 326-record
  manifest.
- A handful of transient `ERR_INTERNET_DISCONNECTED` / `ERR_NAME_NOT_RESOLVED` network drops,
  one navigation-timeout recovery check, one browser-context crash, and a few font-load
  screenshot timeouts occurred across the multi-batch run — every one was resolved by the
  collector's own retry or a later `--resume` pass, never worked around. `manifest.csv`
  reflects only the final, successful state per query; no historical transient failure is
  recorded as permanent.

## Known limitations

- Point-in-time snapshot (2026-08-01/02); Google Images results change constantly and will
  differ on a re-run.
- This is a single first-viewport screenshot per query, not a ranked/scored result list — no
  `organic_rank` or relevance label exists for this evidence (consistent with the 326-query
  benchmark's existing scope: `evaluations.csv` scores Curify only, never Google).
- Screenshots may incidentally display third-party publicly-visible web content (product
  listings, images, page titles) as it appeared in Google's index at capture time; this content
  is not owned by Curify and is included as search-results evidence only, not for
  redistribution or training — see the repository root `DATASET_CARD.md` licensing section.
