# Image rights and attribution review

This document reviews what license/rights status actually applies to each category of content in
this repository, following the addition of the 62-image cross-platform evidence set in
`data/68-query/images/`. It intentionally does **not** relicense third-party content more broadly
than is defensible — see "Open question flagged, not resolved" at the end.

## What CC BY 4.0 actually covers here

The repository's `LICENSE` (CC BY 4.0) is authored-content licensing. It legitimately covers content
Curify actually authored or has rights to license:

- Query text lists (`queries.csv` for both benchmarks) — Curify's own curated/collected query bank.
- Schemas, provenance records, methodology docs, and all `.md` documentation in this repo.
- Evaluation labels and LLM-judge output (`automated_relevance_labels.csv`, `evaluations.csv`,
  `results.jsonl` label/reason fields) — Curify-generated annotations over Curify's own search
  results and (for the `visual_curify_label` fields) Curify's own product screenshots.
- The gallery HTML/JS, `image_manifest.json`, and validation scripts — original code/tooling
  written for this release.

## What CC BY 4.0 does NOT cover

**The 62 screenshot images in `data/68-query/images/{bing,google,canva,pinterest}/` (50 of the 62
files) are screenshots of third-party platforms' search-result pages.** These depict:

- Bing's and Google's search-results page layout, chrome, and the third-party images/content those
  engines indexed and displayed (photographs, illustrations, fan art, product photography, etc.,
  authored by parties unrelated to Curify).
- Canva's and Pinterest's own product UI, plus the templates/pins/images their own users or
  catalogs created.

**None of this is Curify's content to relicense under CC BY 4.0, and this repository does not
purport to do so.** `LICENSE` has been updated with an explicit scope carve-out: the third-party
images are included as benchmark evidence only, copyright remains with the original rights holders
(the platforms and/or the original content creators depicted), and no license to reuse, retrain on,
resell, or redistribute those images independently of this benchmark is granted.

The remaining 12 of 62 images (`data/68-query/images/curify/`) are screenshots of Curify's *own*
product — Curify has clear rights to publish these, and they are covered by CC BY 4.0 like the rest
of the repository's authored content.

## Rationale for including third-party screenshots at all

Including a small (50-image), clearly-labeled set of third-party SERP screenshots as comparative
benchmark evidence — not redistributing the underlying platform catalogs, not bulk-scraping, not
offering the images for downstream training or resale — is a narrow, evaluation-oriented use
consistent with how search-quality and competitive-benchmarking research is commonly conducted and
published. This document records that rationale but is not a substitute for the user's own legal
review before further redistribution; see "Recommendations" below.

## Source URLs and provenance

Where a source URL was actually recorded, it is preserved: the Curify `search_url` for each of the
12 queries is published in `automated_relevance_labels.csv` and echoed in `results.jsonl`'s
`source_page_url` field for the `curify` platform rows. No equivalent per-image search URL exists in
the source data for the four competitor platforms (Bing/Google/Canva/Pinterest) — `source_page_url`
and `image_source_url` are `null` for those 50 records rather than reconstructed or guessed. See
`data/68-query/IMAGE_MAPPING_REPORT.md` for the full field-availability accounting.

## Recommendations for downstream users

1. Do not present the third-party screenshots as CC BY 4.0-licensed, Curify-owned, or freely
   reusable outside of citing/discussing this benchmark.
2. Do not use the screenshots to reconstruct, redistribute, or resell the underlying Bing/Google/
   Canva/Pinterest catalogs.
3. Do not use the screenshots as training data for models without your own independent legal review
   — this repository does not grant that right and neither does CC BY 4.0 for this specific content.
4. When citing example images (e.g. in a paper, blog post, or slide), attribute the platform shown
   in the screenshot, not just "Curify Visual Search Benchmark."

## Open question flagged, not resolved

The existing CC BY 4.0 `LICENSE` file is a single, repo-wide license grant; strictly, a
multi-license repository (one license for authored data/code, "included as evidence, rights
reserved by others" for the third-party images) is better served by a `NOTICE`-style dual-license
structure than a single `LICENSE` file with an internal carve-out paragraph. The carve-out approach
taken here (editing `LICENSE` in place to add a scope-limiting paragraph, rather than inventing a
new, more permissive blanket license for the images) was chosen as the safer of the two available
options without over-engineering a new licensing scheme unilaterally. If the user wants a more
formal split (e.g. a separate `LICENSE-images` or `NOTICE` file, or legal counsel review of the
fair-use rationale above), that is a decision for the user/counsel, not something resolved
automatically here.
