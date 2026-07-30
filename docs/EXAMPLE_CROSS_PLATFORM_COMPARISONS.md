# Example cross-platform comparisons

Eight of the 12 queries with published cross-platform image evidence (see
[`68_IMAGE_SOURCE_INVENTORY.md`](68_IMAGE_SOURCE_INVENTORY.md)), selected for full 5-platform
coverage and a clear, well-documented qualitative contrast between Curify and the competitor
platforms. All 12 available queries have equally "complete" mapping (confirmed query_id/platform,
all 5 platforms present) — this subset was chosen for variety of failure pattern, not because the
other 4 are weaker. Labels and reasons below are copied/lightly trimmed from the published
`results.jsonl`, not re-scored or reworded to look more dramatic.

Browse the actual images at [`../data/68-query/gallery/index.html`](../data/68-query/gallery/index.html)
(filter by `query_id` to jump straight to any case below).

---

### 1. `q002` — "NCT Dream photocard template" (en, 文创)

**Why representative:** an IP/fandom-specific query (K-pop photocard templates) — the clearest kind
of case where a generic embedding can latch onto the wrong sense of a word ("dream").

- **Curify — FAIL.** Decomposed the query down to the bare word "dream" and returned Chinese
  classic-literature illustrations ("Dream of the Red Chamber") and mythological figures — zero
  K-pop or photocard content.
- **Bing** — abundant, correctly-branded NCT Dream photocard templates.
- **Google** — real NCT Dream photocard templates (Instagram/Pinterest/Reddit/X sourced).
- **Canva** — real K-pop photocard templates in the right format, but not NCT Dream-branded.
- **Pinterest** — the most precisely branded match of the four (best competitor platform).

Gallery: filter `query_id = q002`.

---

### 2. `q034` — "Amazon EBC enhanced brand content layout" (en, 营销电商)

**Why representative:** the single strongest gap in the batch — a literal zero-result on Curify for
a mature, well-served design category.

- **Curify — FAIL** (`zero_result`). Literal "No results" page with only generic topic-browse tiles
  as fallback; no query broadening attempted at all.
- **Bing / Google** — abundant, precisely on-topic Amazon EBC/A+ Content design listings.
- **Canva** — manually re-captured; thematically adjacent Amazon listing templates, partial match.
- **Pinterest** — a pin literally titled "EBC / A+ Content" — an exact-category match.

Gallery: filter `query_id = q034`.

---

### 3. `q068` — "zones of regulation poster classroom" (en, 教育)

**Why representative:** the single most unanimous case in the batch — all four competitor platforms
agree, and clearly outperform Curify.

- **Curify — FAIL.** Returned generic K-12 vocabulary/phonics content with zero reference to the
  Zones of Regulation SEL framework.
- **Bing / Google / Canva / Pinterest** — all four return exact "Zones of Regulation"
  posters/worksheets with the correct Blue/Green/Yellow/Red framework. Four-way tie, described in
  the source notes as "the single strongest, most unanimous case in the batch."

Gallery: filter `query_id = q068`.

---

### 4. `q006` — "genshin impact Furina fanart wallpaper 4k" (en, 文创)

**Why representative:** the one case in the batch with a genuine, platform-specific *content* gap
(Canva) rather than a pure *retrieval* gap — useful for illustrating that not every competitor
always wins.

- **Curify — FAIL.** Returned Studio Ghibli stills ("Totoro", "Howl's Moving Castle") instead of any
  Genshin Impact content — a real IP/content gap, not just a decomposition slip.
- **Bing / Google / Pinterest** — abundant, precisely on-topic Furina fanart wallpapers.
- **Canva — genuine content gap.** Matched only generic words ("Impact", "wallpaper") with zero
  actual Genshin/Furina content — Canva's template marketplace doesn't carry licensed-anime fan art,
  confirmed unchanged on a manual re-capture.

Gallery: filter `query_id = q006`.

---

### 5. `q010` — "光与夜之恋 卡面设计参考图" (zh, 文创)

**Why representative:** a Chinese-language IP query with a mid-review correction — shows the
process catching and fixing its own mistake rather than just reporting a clean win/loss.

- **Curify — FAIL.** Zodiac cards, movie fan art, AI/ML infrastructure diagrams — zero connection to
  the game or character-card design.
- **Bing / Google / Pinterest** — abundant exact official/fan character-card art for this specific
  game.
- **Canva — corrected finding.** The original logged-out automated capture showed a hard zero-result
  page ("genuine content gap"). A manual, logged-in re-capture overturned that: Canva's search layer
  correctly recognized the game and its named characters, but the actual template inventory had no
  matching card designs — revised to "partial recognition, no matching inventory," a milder issue
  than a hard content gap.

Gallery: filter `query_id = q010`.

---

### 6. `q009` — "低饱和国风茶包装设计" (zh, 文创)

**Why representative:** the same logged-out-vs-logged-in correction pattern as `q010`, on a
completely different query (packaging design, not a game IP) — shows the correction wasn't a
one-off fluke.

- **Curify — FAIL.** Returned generic, saturated-color Western grocery photography (oats, cookies,
  pasta sauce) — no Chinese-style ("国风") tea packaging, and no low-saturation aesthetic anywhere.
- **Bing / Google / Pinterest** — abundant real 国风 tea-packaging designs matching the requested
  low-saturation aesthetic.
- **Canva — corrected finding.** Logged-out capture showed a zero-result page; a logged-in
  re-capture instead showed the *same* generic grocery-product categories Curify itself returned —
  revised from "content gap" to "generic/imprecise match, same decomposition weakness as Curify."

Gallery: filter `query_id = q009`.

---

### 7. `q015` — "K-beauty glass skin brand launch visual" (en, 品牌)

**Why representative:** a four-way unanimous win for the competitors, and the one query in this
release with extra backup capture files (useful for illustrating the manifest's duplicate/backup
handling).

- **Curify — FAIL.** Baby-care cards, an eyemask, a coffee maker, packaged food — a fully unrelated
  consumer-product grab-bag with no K-beauty or skincare content.
- **Bing / Google / Canva / Pinterest — four-way tie, all strong.** Real, on-topic K-beauty
  "glass skin" brand-launch imagery on every competitor platform.
- **Manifest note:** this query's `curify.png` is byte-identical (same SHA-256) to a retained backup
  file `curify1.png`; a second backup `curify2.png` (a scrolled-view capture) is also published. See
  `IMAGE_MAPPING_REPORT.md` "Duplicate images."

Gallery: filter `query_id = q015`.

---

### 8. `q064` — "maker space label set printable" (en, 教育)

**Why representative:** the one case where a competitor (Canva) shows the *same* failure mode as
Curify, rather than a clean win — useful for showing the benchmark doesn't only publish flattering
competitor comparisons.

- **Curify — FAIL.** Matched the literal word "space" (outer-space/astronomy content) instead of the
  compound term "maker space" — zero label/printable content.
- **Bing / Google / Pinterest** — abundant, precisely on-topic "Makerspace Labels" / "STEM Labels"
  products.
- **Canva** — also matched the literal word "space" (astronaut folder labels, rocket name tags) —
  "the same decomposition weakness Curify shows, though visually coherent." Not a clean sweep for
  the competitors.

Gallery: filter `query_id = q064`.

---

## What this subset does and doesn't show

These 8 (and the 4 not profiled here — `q016`, `q046`, `q053`, `q060`) were all drawn from the same
12-query pilot, which was itself scoped to queries already flagged as likely-problematic for Curify
(see `queries.csv` `planned_test_type`/`likely_recall_challenge` columns) — **all 12 have a Curify
`FAIL` label**. This is a real property of which 12 queries happened to get cross-platform
screenshots, not a cherry-picked "worst 12 of 68" narrative choice by this release; see
`docs/68_IMAGE_SOURCE_INVENTORY.md` for how the 12 were originally selected in the source repo. Do
not read these 8 (or the other 4) as representative of Curify's overall 68-query performance — the
full picture (43 FAIL / 25 WARN / 0 PASS across all 68) is in `data/68-query/automated_relevance_labels.csv`.
