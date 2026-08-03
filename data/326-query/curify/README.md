# Curify screenshot evidence — 326-query set

Real, unedited Curify (`curify-ai.com`) search-results screenshots for all 326 queries in
[`../queries.csv`](../queries.csv) (`query_id` `V001`-`V326`). This is **visual evidence of what
Curify's own search actually returned**, captured 2026-08-02/03 — not a relevance judgment, not a
score, and not a re-run of `evaluations.csv` (which scores two different, earlier Curify code-state
captures from 2026-07-21/22 — see [`../../../METHODOLOGY.md`](../../../METHODOLOGY.md)).

## At a glance

- **Coverage:** 326 of 326 queries (100%), 0 failures.
- **318** are standard `/search?q=...` results pages.
- **1** (`V078`, "bobblehead") is a genuine zero-result search page — a real product response
  (`page_type=search_zero_results`), not a technical failure.
- **7** trigger a deterministic client-side redirect in Curify's own frontend from
  `/search?q=...` to a `/topics/<name>` category page for certain single generic words. The
  screenshot for each captures that actual `/topics/...` page (`page_type=topic_redirect`) — real
  evidence of that product behavior, never worked around, blocked, or forced to a different route.
- **Format:** JPEG, quality 80, exactly 1440x900, single first-viewport screenshot.

## The 7 topic-redirect queries

| query_id | query | redirected to | capture_method |
|---|---|---|---|
| V012 | character | `/topics/character` | `automated_retry` |
| V084 | logo | `/topics/branding` | `automated_retry` |
| V168 | flyer | `/topics/posters` | `automated_retry` |
| V248 | flashcard | `/topics/vocabulary` | `automated_retry` |
| V253 | 地图 | `/topics/map` | `automated_retry` |
| V254 | map | `/topics/map` | `automated_retry` |
| V300 | vocabulary card | `/topics/vocabulary` | `automated_retry` |

These 7 were first collected in the same run as the other 319 (2026-08-02) and correctly recorded
as `status=failed` there, because that collector explicitly refuses to treat a mid-flight redirect
as a "search results" success. A second, narrowly-scoped automated pass (2026-08-03) let the
redirect complete naturally and captured the resulting `/topics/...` page as real evidence — every
one of the 7 was individually, visually verified (page rendered, results grid present and
topically consistent with the query, correct final URL, no error/blank/loading page) before being
marked `status=success` here. They are explicitly tagged `page_type=topic_redirect` and
`capture_method=automated_retry` in `manifest.csv`, kept distinct from the 318
`page_type=search_results` / `capture_method=automated` standard captures — never presented as a
standard search-results page.

**Known exception, all 7 (`exception_type=stale_search_box_text`):** on these `/topics/...` pages,
Curify's own search input displays a rotating placeholder suggestion (confirmed, across repeated
captures of the same query, to show a *different* random string each time) instead of the literal
query text. This is genuine Curify client-side behavior on this page type — not a collection
artifact, not cached/stale browser state, and the page was never edited or DOM-modified to work
around it. It does not affect the validity of the evidence: what was verified is the page body,
results grid, and final URL, all of which correspond to the query.

No manual (non-automated) screenshot is included in this published evidence. An earlier
user-supplied manual capture for these same 7 queries was found on verification to not meet spec
(wrong file format, wrong dimensions, and a search-box mismatch on 2 of 7) and was **not**
published — see the internal `RUN_CONTEXT.md` referenced in `provenance.json` for that history.
Every one of the 7 published screenshots here was produced by the automated retry script, not by
hand.

## Files

| File | Rows | Description |
|---|---|---|
| `manifest.csv` / `manifest.jsonl` | 326 each | One row per query. Field-for-field identical between the two formats. |
| `failed_queries.csv` | 0 data rows | Header only — no query is in a failed state in this published evidence. |
| `screenshots/` | 326 JPEGs | `V001__query.jpg` style filenames (query_id + ASCII slug; non-ASCII-only queries fall back to a `query` placeholder slug, e.g. `V253__query.jpg` for "地图" — `query_id` is always the authoritative key). |
| `gallery.html` | - | Offline, self-contained gallery — open directly in a browser, no server needed. |

## Manifest fields

`query_id, source_row, query, platform, search_url, screenshot_path, status, page_status,
result_count_observed, attempt_count, started_at, completed_at, duration_ms, error_type,
error_message, collector_version, input_sha256, requested_search_url, final_url, page_type,
redirect_detected, redirect_target, capture_method, capture_status, exception_type`

- `platform` is always `curify`.
- `page_type`: `search_results` (318), `search_zero_results` (1, `V078`), or `topic_redirect` (7).
- `capture_method`: `automated` (319, original 2026-08-02 run) or `automated_retry` (7, 2026-08-03
  targeted retry). No row has a manual capture method in this published evidence.
- `requested_search_url` is always the literal `/search?q=...` URL requested; `final_url` differs
  from it only for the 7 `topic_redirect` rows.
- `input_sha256` matches `../queries.csv`'s SHA-256 (`d8ae0f4ef77567b4dcf8f15635b11c140810c3b991a8134a99997e11ad6a1d9e`) on every row.

## Collection method

- Playwright, Chromium, headed, plain (non-persistent) `newContext()` per browser context — no cookies,
  history, or profile persisted; viewport/screenshot 1440x900; concurrency 1; random 3,000-7,000ms
  delay between queries (main run); 45,000ms navigation timeout.
- Results-loaded detection: race between a result-card selector and an explicit zero-result-text
  selector, then a network-idle wait plus a poll confirming every visible result-card image has
  finished loading before the screenshot.
- The 7 topic-redirect queries: up to 3 attempts each in a fresh browser context, letting Curify's
  own client-side redirect complete naturally — never intercepted, blocked, or given a different
  route.
- No CAPTCHA, consent wall, or bot-detection was ever encountered against Curify in either
  collection pass.

## Known limitations

- Point-in-time snapshot (2026-08-02/03); Curify's live search has likely changed since.
- This is a single first-viewport screenshot per query, not a scored or ranked result list — no
  relevance label exists for this evidence (the existing `evaluations.csv` LLM-judge scores are
  from separate, earlier 2026-07-21/22 captures and were not re-generated from these screenshots).
- The 7 `topic_redirect` pages show Curify's category-browsing UI, not a literal search-results
  list — read them as "what Curify actually shows for this query," not as a ranked result set.
